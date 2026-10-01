from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet


@dataclass(frozen=True)
class CallRequest:
    mode: str
    destination: str
    self_calls_enabled: bool = False
    live_calls_enabled: bool = False
    calls_enabled: bool = False
    ai_cold_call_policy: str = "blocked"
    disclosure_enabled: bool = False
    contains_phi: bool = False
    on_dnc: bool = False
    daily_count: int = 0
    daily_limit: int = 1
    allowed_self_numbers: FrozenSet[str] | set[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str


def decide(request: CallRequest) -> Decision:
    if request.contains_phi:
        return Decision(False, "sales_call_contains_phi")

    if request.on_dnc:
        return Decision(False, "destination_is_suppressed")

    if request.daily_limit < 1 or request.daily_count >= request.daily_limit:
        return Decision(False, "daily_limit_reached")

    if request.mode == "self_call":
        if not request.self_calls_enabled:
            return Decision(False, "self_calls_disabled")
        if request.destination not in set(request.allowed_self_numbers):
            return Decision(False, "self_destination_not_allowlisted")
        return Decision(True, "self_call_allowed")

    if request.mode == "live_prospect":
        if not request.calls_enabled:
            return Decision(False, "global_sales_calls_disabled")
        if not request.live_calls_enabled:
            return Decision(False, "live_sales_calls_disabled")
        if request.ai_cold_call_policy != "approved":
            return Decision(False, "ai_cold_call_policy_not_approved")
        if not request.disclosure_enabled:
            return Decision(False, "ai_disclosure_missing")
        return Decision(True, "live_call_policy_satisfied")

    return Decision(False, "unknown_call_mode")
