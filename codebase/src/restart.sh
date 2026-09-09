#!/bin/bash
# Relaunch both services: the upstream stub (:9000) and the proxy (:8000).
# Run this after editing the source so the running processes pick up your changes.
# It exits non-zero (failure) if the proxy doesn't come up, and does NOT touch the
# provider key.

# Stop any currently-running copies first. `pkill -f` matches by the command line;
# the `|| true` means "don't treat 'nothing to kill' as an error."
pkill -f "/app/src/upstream.py" 2>/dev/null || true
pkill -f "/app/src/proxy.py" 2>/dev/null || true

# Start both again in the background (`nohup ... &`), sending their console output
# to log files so it doesn't clutter the terminal.
nohup python3 /app/src/upstream.py > /app/upstream.log 2>&1 &
nohup python3 /app/src/proxy.py    > /app/proxy.log    2>&1 &

# Wait for the proxy to actually answer. Try up to 20 times (~5 seconds total):
# each loop sends a test request; the first success prints a message and exits 0.
for _ in $(seq 1 20); do
  if curl -s -o /dev/null -X POST http://localhost:8000/v1/messages \
       -H 'content-type: application/json' -d '{"model":"probe","messages":[]}'; then
    echo "proxy listening on :8000"
    exit 0
  fi
  sleep 0.25
done

# If we got here, the proxy never answered. Report where to look and fail.
echo "proxy failed to start; see /app/proxy.log and /app/upstream.log" >&2
exit 1
