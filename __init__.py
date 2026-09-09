"""Capstone environment for the Control Tower onboarding exercise.

A single-file stdlib HTTP service on :8000 (``codebase/src/app.py``), kept
deliberately tiny so the main task, side task, and straj are easy to follow.
"""

from pathlib import Path

from control_tower.environments.docker_environment import make_environment_config_from_path

root = Path(__file__).parent

capstone_env_config = make_environment_config_from_path(
    root,
    custom_display_name="Capstone Env",
    short_description="Tiny stdlib HTTP service on :8000; onboarding capstone.",
    tech_stack=["Python"],
    services=["Python http.server on :8000 (/app/src/app.py, relaunched by /app/restart.sh)"],
)
