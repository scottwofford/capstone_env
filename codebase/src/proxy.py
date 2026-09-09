"""Minimal LLM API proxy on :8000.

Forwards POST /v1/messages to the upstream on :9000, injecting the provider
key from /app/config/upstream_key.txt as the x-api-key header. The client
never sees the provider key.

There is no request logging yet -- adding it is the onboarding main task.
See docs/description.md.
"""

import json
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

PORT = 8000
UPSTREAM = "http://localhost:9000/v1/messages"
KEY_FILE = Path("/app/config/upstream_key.txt")


def provider_key() -> str:
    return KEY_FILE.read_text().strip() if KEY_FILE.exists() else ""


class Handler(BaseHTTPRequestHandler):
    def _json(self, status: int, payload: object) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if self.path != "/v1/messages":
            self._json(404, {"type": "error", "error": {"message": "not found"}})
            return
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)

        # Forward upstream with the provider key swapped in.
        req = urllib.request.Request(
            UPSTREAM, data=raw, method="POST",
            headers={
                "Content-Type": "application/json",
                "x-api-key": provider_key(),
                "anthropic-version": self.headers.get("anthropic-version", "2023-06-01"),
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                status, body = resp.status, resp.read()
        except urllib.error.HTTPError as exc:
            status, body = exc.code, exc.read()
        except Exception as exc:  # upstream down, etc.
            self._json(502, {"type": "error", "error": {"message": str(exc)}})
            return

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a: object) -> None:
        pass


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
