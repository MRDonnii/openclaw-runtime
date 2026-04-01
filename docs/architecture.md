# OpenClaw Architecture: Generic vs Domain-Specific

This document describes the architectural boundary between the generic OpenClaw runtime and domain-specific adapter logic.

---

## The two layers

### Layer 1: Generic runtime (this repo)

The generic runtime handles everything that is the same regardless of which domain (heating, Tesla, energy) is being used:

- **Request envelope**: a standard `OpenClawRequest` carries domain name, request ID, prompt, and payload.
- **Result envelope**: a standard `OpenClawResult` carries the domain name, request ID, raw response text, and parsed data.
- **Adapter spec**: each domain declares a `DomainAdapterSpec` describing its endpoints, prompt header, model preference, and output schema.
- **Model preference**: each adapter declares its preferred provider and model, plus fallback models.
- **Path conventions**: shared path constants for session directories, result files, and state files.

None of this is heating-specific. It can be reused for any AI decision flow.

### Layer 2: Domain adapter (stays in domain repo)

Each domain provides the integration-specific layer:

- **Payload builder**: collects data from HA sensors, energy APIs, Tesla API, etc. and assembles the input payload.
- **Bridge endpoint**: a route like `/heating/decision` or `/tesla/decision` that receives the domain request.
- **Callback handler**: a route like `/heating/callback/<request_id>` that receives the resolved result.
- **Output consumer**: updates HA entities, sensors, automations, and reports based on the result.
- **Validation**: domain-specific output validation (e.g., heating `factor` must be between 0.6 and 1.4).

---

## How the bridge/worker pattern works

See [bridge_pattern.md](bridge_pattern.md) for the full runtime flow.

---

## Current adapters

| Adapter   | Status          | Repo                              |
|-----------|-----------------|-----------------------------------|
| heating   | In production   | [ai-varme-styring](https://github.com/MRDonnii/ai-varme-styring) — `custom_components/ai_varme_styring` |
| tesla     | Spec only       | Documented in `domains/` here     |

---

## Design principles

1. **Generic stays generic**: do not add heating or Tesla semantics to `contracts.py` or `paths.py`.
2. **Adapters are isolated**: each domain adapter has its own endpoint, schema, and HA entities.
3. **Model preference is per adapter**: the adapter declares what it wants; OpenClaw routing handles delivery.
4. **No cross-adapter contamination**: Tesla charging decisions must never appear in heating responses and vice versa.
