# openclaw-runtime

A reusable runtime and tool layer for OpenClaw-based AI flows in Home Assistant.

This repo contains the shared foundation that domain adapters are built on top of.
It is **not** the full Home Assistant heating integration — it is the generic layer underneath it.

---

## What is this?

OpenClaw is a local AI runtime that connects Home Assistant automations to structured AI decisions.
This repo holds the **generic runtime layer**: the request/result contracts, path conventions, and domain adapter specs that any OpenClaw-powered integration can share.

The first domain adapter is **heating** (`heating`), which is implemented and running in production in [ai-varme-styring](https://github.com/MRDonnii/ai-varme-styring) under `custom_components/ai_varme_styring`.
The second planned adapter is **tesla**, which is specified here but not yet implemented.

---

## What is generic, and what is domain-specific?

### Generic (this repo)

- Request/result data contracts (`OpenClawRequest`, `OpenClawResult`)
- Domain adapter spec structure (`DomainAdapterSpec`)
- Model preference per adapter (`ModelPreference`)
- Output schema contract per adapter (`OutputSchemaSpec`)
- Shared filesystem path conventions (`paths.py`)
- Adapter spec instances (`HEATING_ADAPTER_SPEC`, `TESLA_ADAPTER_SPEC`)

### Domain-specific (stays in HA config)

- The actual bridge script (`openclaw_decision_bridge.py`)
- The session completion worker (`openclaw_session_completion_worker.py`)
- Home Assistant custom component (`custom_components/ai_varme_styring`)
- Payload builders, entity sensors, automations, and HA service calls
- Route definitions: `/heating/decision`, `/heating/callback/<request_id>`

---

## Model preference strategy

Each adapter declares its preferred model in `ModelPreference`:

| Adapter   | Provider         | Model       | Fallback  |
|-----------|------------------|-------------|-----------|
| heating   | github-copilot   | gpt-5-mini  | gpt-4.1   |
| tesla     | github-copilot   | gpt-5-mini  | gpt-4.1   |

`gpt-4o` is intentionally excluded from this strategy.

This preference is documented in the adapter spec. Actual model routing in OpenClaw is a separate concern handled at the OpenClaw side.

---

## Current status

This is a first foundation release. It captures the shared layer that already underlies the live heating integration.

- **Heating**: implemented, running in production (`custom_components/ai_varme_styring` in [ai-varme-styring](https://github.com/MRDonnii/ai-varme-styring))
- **Tesla**: specified and documented here, not yet implemented
- **Energy / other**: not yet specified

This is a clean foundation, not a finished multi-domain production platform.

---

## No npm dependency

This runtime is pure Python. No npm, no Node.js dependency.

---

## Repo layout

```
openclaw-runtime/
  README.md                        # this file
  docs/
    architecture.md                # generic vs domain-specific architecture
    bridge_pattern.md              # how the bridge/worker pattern works
  openclaw_runtime/
    __init__.py
    README.md                      # internal notes on structure
    contracts.py                   # shared contracts and adapter specs
    paths.py                       # shared path conventions
    domains/
      README.md                    # domain adapter overview
      tesla_adapter_spec.md        # Tesla adapter spec (not yet implemented)
```

---

## Source of truth

The `openclaw_runtime/` source code in this repo is authored and maintained in:

```
/haconfig/tools/openclaw_runtime
```

inside the [ai-varme-styring](https://github.com/MRDonnii/ai-varme-styring) repo. This standalone GitHub repo is the published extraction of that layer.
If the two ever diverge, `/haconfig/tools/openclaw_runtime` is authoritative.

## Related repos

- [ai-varme-styring](https://github.com/MRDonnii/ai-varme-styring): the full Home Assistant config repo. Contains the live heating integration (`custom_components/ai_varme_styring`), the bridge/worker scripts (`tools/`), and the OpenClaw runtime source (`tools/openclaw_runtime/`).

---

## License

Internal use. No license declared yet.
