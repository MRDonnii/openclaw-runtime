# OpenClaw Bridge/Worker Pattern

This document describes the runtime flow used by domain adapters to get AI decisions from OpenClaw and deliver them back to Home Assistant.

The pattern was designed and first proven in the heating integration.
It can be reused for any new domain adapter.

---

## Components

| Component                          | Role                                                                 |
|------------------------------------|----------------------------------------------------------------------|
| Domain integration (HA component)  | Builds payload and sends request to bridge                           |
| `openclaw_decision_bridge.py`      | Receives domain request, submits to OpenClaw, tracks pending request |
| `openclaw_session_completion_worker.py` | Polls OpenClaw session files, extracts completed AI result     |
| Worker → Bridge callback           | Worker posts resolved result back to bridge                          |
| Bridge → HA callback               | Bridge resolves the pending request and returns result to HA         |

---

## Request flow

```
HA domain integration
  → POST /heating/decision (or /tesla/decision)
    → Bridge submits to OpenClaw, receives runId
      → Completion worker watches OpenClaw session files
        → Worker finds final assistant JSON
          → Worker POSTs to /heating/callback/<request_id>
            → Bridge resolves pending request
              → HA receives structured JSON result
```

---

## What is generic in this pattern

- Bridge request/callback handling (request ID correlation, pending resolution)
- Session completion worker (OpenClaw session file polling and parsing)
- Result/state files (`_tmp_openclaw_completion_results.json`, etc.)
- Watchdog startup and health handling

## What is domain-specific

- Route: `/heating/decision` vs `/tesla/decision`
- Callback route: `/heating/callback/<request_id>` vs `/tesla/callback/<request_id>`
- Prompt header (defined in adapter spec)
- Output schema and validation rules (defined in adapter spec)
- HA entity updates after result is received

---

## Runtime hosting

The bridge and completion worker run as persistent processes on the Home Assistant host.
They are managed via a watchdog script (`openclaw_services_ensure.sh`) and optionally systemd units.

The host runs under `s6` supervision (not standard systemd PID 1), so the watchdog cron approach is used for reliable startup and self-healing.

---

## Files (live in HA config, not this repo)

- `/haconfig/tools/openclaw_decision_bridge.py`
- `/haconfig/tools/openclaw_session_completion_worker.py`
- `/haconfig/tools/openclaw_bridge_ctl.sh`
- `/haconfig/tools/openclaw_completion_worker_ctl.sh`
- `/haconfig/tools/openclaw_services_ensure.sh`
- `/haconfig/tools/systemd/` (env files and service units)
- `/haconfig/packages/openclaw_bridge_callback.yaml` (HA package for callback wiring)

These script files are domain-adapter-aware (currently heating-first) but follow the generic pattern described here.
