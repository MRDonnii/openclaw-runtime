"""Shared filesystem paths for OpenClaw runtime helpers."""

from __future__ import annotations

import os
from pathlib import Path


OPENCLAW_APPDATA = Path(os.environ.get("OPENCLAW_APPDATA_DIR", "/openclaw-data/config"))
OPENCLAW_SESSIONS_DIR = Path(
    os.environ.get(
        "OPENCLAW_SESSIONS_DIR",
        str(OPENCLAW_APPDATA / "agents" / "main" / "sessions"),
    )
)

HA_CONFIG_DIR = Path(os.environ.get("HA_CONFIG_DIR", "/haconfig"))
OPENCLAW_RESULTS_FILE = Path(
    os.environ.get(
        "OPENCLAW_COMPLETION_RESULTS_FILE",
        str(HA_CONFIG_DIR / "_tmp_openclaw_completion_results.json"),
    )
)
OPENCLAW_STATE_FILE = Path(
    os.environ.get(
        "OPENCLAW_COMPLETION_STATE_FILE",
        str(HA_CONFIG_DIR / "_tmp_openclaw_completion_worker_state.json"),
    )
)
OPENCLAW_BRIDGE_LOG = HA_CONFIG_DIR / "_tmp_openclaw_bridge.log"
OPENCLAW_WORKER_LOG = HA_CONFIG_DIR / "_tmp_openclaw_completion_worker.log"
