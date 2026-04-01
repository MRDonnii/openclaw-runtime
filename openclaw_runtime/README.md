# OpenClaw Runtime Core

Denne mappe er tænkt som den fælles runtime-kerne for OpenClaw-baserede flows i Home Assistant.

## Formål

Skille den generiske OpenClaw-infrastruktur fra domænespecifik logik som:
- varmestyring
- Tesla-flows
- energioptimering
- ventilation / fugtighed

## Princip

Det der bør være fælles:
- request-id korrelation
- session/completion lookup
- resultatlevering
- logging og state tracking
- adapter-kontrakt for domæner
- model-præference og prompt-header per adapter
- output-schema per adapter

Det der bør være domænespecifikt:
- payload-opbygning
- output-schema
- Home Assistant entities / rapportvisning
- handlinger og automations

## Nuvarande status

Den aktive varmestyring bruger stadig de varme-specifikke scripts:
- `/haconfig/tools/openclaw_decision_bridge.py`
- `/haconfig/tools/openclaw_session_completion_worker.py`

Denne mappe er et sikkert næste skridt, så vi kan begynde at samle fælles kode uden at risikere den kørende varme-stack.

## Foreslået retning

1. flyt fælles hjælpefunktioner hertil
2. behold `heating` som første adapter
3. tilføj senere en `tesla` adapter
4. lad gamle OpenClaw workspace scripts være ikke-autoritative referencer

## Mapper

- `contracts.py`
  Fælles datatyper og kontrakter for OpenClaw requests/results.
  Indeholder nu også:
  - `ModelPreference`
  - `OutputSchemaSpec`
  - `HEATING_ADAPTER_SPEC`
  - `TESLA_ADAPTER_SPEC`

- `paths.py`
  Fælles stier for sessions, logs og result/state filer.

- `domains/`
  Adapter-specs og senere adapterkode per domæne.

## Model-præference

Hver adapter bør kunne angive:
- foretrukken provider
- foretrukken model
- eventuelle fallback-modeller
- om JSON skal være strikt
- hvilken reasoning-profil der ønskes

Eksempel i denne struktur:
- heating foretrækker `github-copilot / gpt-5-mini`
- tesla foretrækker også `github-copilot / gpt-5-mini`
- begge bruger `gpt-4.1` som fallback

`gpt-4o` indgår ikke i denne strategi.

Det betyder ikke, at runtime allerede tvinger modellen i OpenClaw.
Det betyder, at adapteren nu har en tydelig og dokumenteret preference,
som vi senere kan koble til den konkrete OpenClaw model-routing når den del er afklaret.
