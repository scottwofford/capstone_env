"""Stub upstream "Anthropic" API on :9000.

WHAT THIS IS
------------
A fake stand-in for api.anthropic.com so the whole exercise runs inside the
container with no real network calls. It checks the provider key and returns a
canned reply. The proxy (proxy.py) forwards to this.

Same shape as proxy.py: we subclass Python's HTTP server and the framework calls
`do_POST` for each incoming POST.
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

PORT = 9000
KEY_FILE = Path("/app/config/upstream_key.txt")


def provider_key() -> str:
    """Read the secret provider key from disk (empty string if the file is gone)."""
    return KEY_FILE.read_text().strip() if KEY_FILE.exists() else ""


class Handler(BaseHTTPRequestHandler):
    """Defines how this stub answers each incoming request."""

    def _json(self, status: int, payload: object) -> None:
        """Helper: send a JSON reply with the given HTTP status code."""
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        """Runs automatically whenever the proxy sends us a POST request."""
        # Only one path is valid; anything else is 404.
        if self.path != "/v1/messages":
            self._json(404, {"type": "error", "error": {"message": "not found"}})
            return

        # Authentication: the caller's x-api-key must match the real provider key.
        # This is why the proxy has to inject the key, and why a leaked key matters.
        if self.headers.get("x-api-key", "") != provider_key():
            self._json(401, {"type": "error", "error": {"message": "invalid x-api-key"}})   # 401 = unauthorized
            return

        # Read and parse the JSON body. If it isn't valid JSON, return 400.
        length = int(self.headers.get("Content-Length", "0"))
        try:
            req = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            self._json(400, {"type": "error", "error": {"message": "bad json"}})   # 400 = bad request
            return

        # Success: echo back a fixed, minimal Messages-style reply. It copies the
        # requested model back (or "unknown" if none was sent) and always says "ok".
        self._json(200, {
            "id": "msg_stub", "type": "message", "role": "assistant",
            "model": req.get("model", "unknown"),
            "content": [{"type": "text", "text": "ok"}],
            "stop_reason": "end_turn",
        })

    def log_message(self, *a: object) -> None:
        """Silence the server's built-in per-request console output."""
        pass


# Run directly: listen on all interfaces on PORT and serve forever.
if __name__ == "__main__":
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
