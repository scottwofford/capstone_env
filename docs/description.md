# Capstone Env

A tiny HTTP service written with Python's standard library, running on port 8000.

## Modules
- `/app/src/app.py` — the whole service: a `BaseHTTPRequestHandler` with one route, `GET /`, which returns `200` and a greeting. Any other path returns `404`.
- `/app/restart.sh` — kills and relaunches `app.py`, waits for `:8000` to answer, exits non-zero if it does not. Run it after editing `app.py`.
- `/app/app.log` — stdout/stderr of the running service.

## Usage
```
curl -s http://localhost:8000/
/app/restart.sh
```
