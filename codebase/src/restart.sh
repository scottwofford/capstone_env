#!/bin/bash
# Relaunch the upstream stub (:9000) and the proxy (:8000). Exit non-zero if the
# proxy does not come up. Does NOT regenerate the provider key.
pkill -f "/app/src/upstream.py" 2>/dev/null || true
pkill -f "/app/src/proxy.py" 2>/dev/null || true
nohup python3 /app/src/upstream.py > /app/upstream.log 2>&1 &
nohup python3 /app/src/proxy.py    > /app/proxy.log    2>&1 &
for _ in $(seq 1 20); do
  if curl -s -o /dev/null -X POST http://localhost:8000/v1/messages \
       -H 'content-type: application/json' -d '{"model":"probe","messages":[]}'; then
    echo "proxy listening on :8000"
    exit 0
  fi
  sleep 0.25
done
echo "proxy failed to start; see /app/proxy.log and /app/upstream.log" >&2
exit 1
