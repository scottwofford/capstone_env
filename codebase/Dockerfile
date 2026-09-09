FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Common dependencies - git is REQUIRED for gen-traj command,
# python + inspect-tool-support are REQUIRED for the text_editor tool.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    vim \
    nano \
    git \
    procps \
    python3 \
    python3-pip \
    python3-venv \
    sudo \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PATH="$PATH:/opt/inspect_tool_support/bin"
RUN python3 -m venv /opt/inspect_tool_support && \
    /opt/inspect_tool_support/bin/pip install inspect-tool-support && \
    /opt/inspect_tool_support/bin/inspect-tool-support post-install --no-web-browser

WORKDIR /app

# REQUIRED — agents, scorers, and devs call /app/restart.sh directly.
COPY src/ /app/src/
RUN cp /app/src/restart.sh /app/restart.sh && chmod +x /app/restart.sh /app/src/restart.sh

LABEL org.opencontainers.image.source=https://github.com/scottwofford/capstone_env
LABEL org.opencontainers.image.description="capstone environment: tiny stdlib HTTP service"

CMD ["/bin/bash", "-c", "/app/restart.sh; tail -f /dev/null"]
