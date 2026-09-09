#!/bin/bash
# Relaunch the HTTP service on :8000. Exit non-zero if it does not come up.
pkill -f "/app/src/app.py" 2>/dev/null || true
nohup python3 /app/src/app.py > /app/app.log 2>&1 &
for _ in $(seq 1 20); do
  if curl -s -o /dev/null http://localhost:8000/todos; then
    echo "app.py listening on :8000"
    exit 0
  fi
  sleep 0.25
done
echo "app.py failed to start; see /app/app.log" >&2
exit 1
