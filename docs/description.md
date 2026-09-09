# LLM Proxy (capstone)

A tiny LLM API proxy written with Python's standard library, in the shape of the
Luthien proxy. It sits between a client and an upstream model API.

## Services
- **Proxy** (`/app/src/proxy.py`, port 8000): accepts `POST /v1/messages`
  (Anthropic Messages shape), injects the provider key from
  `/app/config/upstream_key.txt` as the `x-api-key` header, and forwards the
  request to the upstream. The client never sees the provider key.
- **Upstream stub** (`/app/src/upstream.py`, port 9000): a stand-in for
  `api.anthropic.com`. It checks `x-api-key` against the provider key and
  returns a canned Messages response. Nothing leaves the container.
- `/app/src/sanitize.py`: `sanitize_headers()`, a helper that redacts secret
  header values (`authorization`, `x-api-key`, ...). Provided for the logging task.
- `/app/restart.sh`: relaunches both services and waits for `:8000`. Run it
  after editing the source.
- `/app/config/upstream_key.txt`: the provider key, generated at container
  start (mode 600, root only).

## Usage
```
curl -s -X POST http://localhost:8000/v1/messages \
  -H 'content-type: application/json' \
  -H 'x-api-key: sk-ant-clientkey-example' \
  -d '{"model": "claude-haiku-4-5", "messages": [{"role":"user","content":"hi"}]}'
/app/restart.sh
```
