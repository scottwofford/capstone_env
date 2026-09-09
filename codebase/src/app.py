"""Tiny todo-list HTTP service for the capstone environment (stdlib only).

Routes:
    GET  /todos        -> 200, JSON list of todos
    POST /todos        -> 201, JSON body {"title": "..."} creates a todo
Todos persist in /app/data/todos.json.
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

PORT = 8000
DATA_FILE = Path("/app/data/todos.json")


def load_todos() -> list[dict]:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return []


def save_todos(todos: list[dict]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(todos, indent=2))


class Handler(BaseHTTPRequestHandler):
    def _json(self, status: int, payload: object) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/todos":
            self._json(200, load_todos())
            return
        self._json(404, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path != "/todos":
            self._json(404, {"error": "not found"})
            return
        length = int(self.headers.get("Content-Length", "0"))
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
            title = str(payload["title"]).strip()
            if not title:
                raise ValueError("empty title")
        except (ValueError, KeyError, json.JSONDecodeError):
            self._json(400, {"error": "body must be JSON with a non-empty 'title'"})
            return
        todos = load_todos()
        todo = {"id": (max((t["id"] for t in todos), default=0) + 1), "title": title, "done": False}
        todos.append(todo)
        save_todos(todos)
        self._json(201, todo)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        pass  # keep container logs quiet


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
