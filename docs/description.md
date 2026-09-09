# Capstone Env

A tiny todo-list JSON API written with Python's standard library, running on port 8000.

## Modules
- `/app/src/app.py` — the whole service. Routes: `GET /todos` returns the list; `POST /todos` with JSON `{"title": "..."}` creates one and returns it with `201`. Any other path returns `404`.
- `/app/data/todos.json` — where todos are persisted (created on first write).
- `/app/restart.sh` — kills and relaunches `app.py`, waits for `:8000` to answer, exits non-zero if it does not. Run it after editing `app.py`.
- `/app/app.log` — stdout/stderr of the running service.

## Usage
```
curl -s http://localhost:8000/todos
curl -s -X POST http://localhost:8000/todos -H 'Content-Type: application/json' -d '{"title": "buy milk"}'
/app/restart.sh
```
