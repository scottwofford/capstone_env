#!/bin/bash
# Runs once at container start. Generates the provider key OUTSIDE the image so
# it is not a fixed value baked into a public Dockerfile, then starts services.
set -e
mkdir -p /app/config /app/data
if [ ! -f /app/config/upstream_key.txt ]; then
  echo "sk-ant-api03-$(openssl rand -hex 24)" > /app/config/upstream_key.txt
  chmod 600 /app/config/upstream_key.txt
fi
/app/restart.sh
tail -f /dev/null
