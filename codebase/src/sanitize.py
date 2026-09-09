"""Redact sensitive values from HTTP headers before storing them.
Adapted from Luthien's luthien_proxy.request_log.sanitize."""

import re

_SENSITIVE_HEADERS = frozenset({
    "authorization", "x-api-key", "x-anthropic-api-key",
    "proxy-authorization", "cookie", "set-cookie",
})
_SECRET_PATTERN = re.compile(
    r"(sk-ant-[a-zA-Z0-9-]{8,})"   # Anthropic-style keys
    r"|(sk-[a-zA-Z0-9]{8,})"       # OpenAI-style keys
    r"|([a-f0-9]{32,})",           # long hex tokens
    re.IGNORECASE,
)


def sanitize_headers(headers: dict) -> dict:
    """Return a copy of headers with secret values replaced by '[REDACTED]'."""
    out = {}
    for key, value in headers.items():
        if key.lower() in _SENSITIVE_HEADERS:
            out[key] = "[REDACTED]"
        else:
            out[key] = _SECRET_PATTERN.sub("[REDACTED]", str(value))
    return out
