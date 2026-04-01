# Tesla OpenClaw Adapter Spec

Dette er en første skitse til et Tesla-flow ovenpå den samme OpenClaw-runtime som varmestyringen.

## Formål

Erstatte eller reducere separate Ollama-flows for Tesla ved at bruge:
- OpenClaw hook
- session/completion worker
- en Tesla-specifik adapter i Home Assistant

## Foretrukken model

Hvis OpenClaw runtime tillader modelvalg pr. adapter, er den foretrukne model:
- provider: `github-copilot`
- model: `gpt-5-mini`
- fallback: `gpt-4.1`

Begrundelse:
- høj kvalitet
- god til strikte JSON-svar
- ønsket om at bruge Copilot-modeller med god tokenøkonomi
- `gpt-4o` holdes ude af denne adapterstrategi

## Input-idé

Muligt payload:
- batteriniveau
- opladestatus
- hjemme/ude
- strømpris nu
- planlagte ture
- ønsket minimum SoC
- tidspunkt til næste afgang
- wall connector / charging state

## Output-idé

Eksempel:

```json
{
  "charge_now": true,
  "target_soc": 80,
  "confidence": 88,
  "reason": "Lav elpris og bilen skal bruges i morgen tidlig."
}
```

## Arkitektur

1. Tesla integration bygger payload
2. OpenClaw modtager request
3. completion worker finder resultat
4. Tesla-adapter validerer output
5. HA opdaterer sensorer / knapper / automations

## Vigtigt

Tesla skal være en separat adapter.
Den må ikke blandes direkte ind i varmestyringens payload eller decision-schema.
