"""Stub upstream 'Anthropic' API on :9000. Verifies the provider key and echoes
a canned Messages response. Stands in for api.anthropic.com so the environment
needs no network."""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

PORT = 9000
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
        if self.headers.get("x-api-key", "") != provider_key():
            self._json(401, {"type": "error", "error": {"message": "invalid x-api-key"}})
            return
        length = int(self.headers.get("Content-Length", "0"))
        try:
            req = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            self._json(400, {"type": "error", "error": {"message": "bad json"}})
            return
        self._json(200, {
            "id": "msg_stub", "type": "message", "role": "assistant",
            "model": req.get("model", "unknown"),
            "content": [{"type": "text", "text": "ok"}],
            "stop_reason": "end_turn",
        })

    def log_message(self, *a: object) -> None:
        pass


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
