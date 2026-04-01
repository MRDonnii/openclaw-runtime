"""Shared OpenClaw runtime contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class OpenClawRequest:
    """Generic request envelope for a domain adapter."""

    domain: str
    request_id: str
    prompt: str
    payload: dict[str, Any] = field(default_factory=dict)
    callback_url: str = ""


@dataclass(slots=True)
class OpenClawResult:
    """Generic normalized result from a domain adapter."""

    domain: str
    request_id: str
    raw_text: str
    data: dict[str, Any] = field(default_factory=dict)
    source: str = ""


@dataclass(slots=True)
class ModelPreference:
    """Preferred model/provider settings for an adapter."""

    provider: str = ""
    model: str = ""
    fallback_models: list[str] = field(default_factory=list)
    strict_json: bool = True
    reasoning_profile: str = "balanced"


@dataclass(slots=True)
class OutputSchemaSpec:
    """Minimal schema contract for an adapter result."""

    required_keys: list[str] = field(default_factory=list)
    optional_keys: list[str] = field(default_factory=list)
    numeric_ranges: dict[str, tuple[float, float]] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class DomainAdapterSpec:
    """Describe a domain adapter in a reusable way."""

    domain: str
    decision_endpoint: str
    callback_endpoint_pattern: str
    prompt_header: str = ""
    model_preference: ModelPreference = field(default_factory=ModelPreference)
    output_schema: OutputSchemaSpec = field(default_factory=OutputSchemaSpec)
    required_keys: list[str] = field(default_factory=list)
    optional_keys: list[str] = field(default_factory=list)


HEATING_ADAPTER_SPEC = DomainAdapterSpec(
    domain="heating",
    decision_endpoint="/heating/decision",
    callback_endpoint_pattern="/heating/callback/{request_id}",
    prompt_header=(
        "You are the heating decision adapter for Home Assistant. "
        "Return strict JSON only. "
        "Assess all rooms mentally, use humidity/comfort data when present, "
        "and only include room overrides when they are necessary."
    ),
    model_preference=ModelPreference(
        provider="github-copilot",
        model="gpt-5-mini",
        fallback_models=["gpt-4.1"],
        strict_json=True,
        reasoning_profile="balanced",
    ),
    output_schema=OutputSchemaSpec(
        required_keys=["factor", "confidence", "reason"],
        optional_keys=["global", "rooms", "request_id"],
        numeric_ranges={
            "factor": (0.6, 1.4),
            "confidence": (0.0, 100.0),
        },
        notes=[
            "Use short Danish reasoning.",
            "Do not claim all rooms are at target if any room has deficit > 0.05 C.",
            "Use room overrides sparingly and conservatively.",
        ],
    ),
)


TESLA_ADAPTER_SPEC = DomainAdapterSpec(
    domain="tesla",
    decision_endpoint="/tesla/decision",
    callback_endpoint_pattern="/tesla/callback/{request_id}",
    prompt_header=(
        "You are the Tesla decision adapter for Home Assistant. "
        "Return strict JSON only. "
        "Optimize charging behavior using price, time window, state of charge, "
        "and departure constraints."
    ),
    model_preference=ModelPreference(
        provider="github-copilot",
        model="gpt-5-mini",
        fallback_models=["gpt-4.1"],
        strict_json=True,
        reasoning_profile="balanced",
    ),
    output_schema=OutputSchemaSpec(
        required_keys=["charge_now", "target_soc", "confidence", "reason"],
        optional_keys=["start_time", "stop_time", "request_id"],
        numeric_ranges={
            "target_soc": (0.0, 100.0),
            "confidence": (0.0, 100.0),
        },
        notes=[
            "Prefer low-price charging windows when practical.",
            "Respect departure time and minimum required state of charge.",
            "Keep the result machine-readable and conservative.",
        ],
    ),
)
