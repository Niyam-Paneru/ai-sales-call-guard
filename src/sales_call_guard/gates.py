from __future__ import annotations

from .models import CallRequest, Decision


def hard_gate(request: CallRequest) -> Decision | None:
    if request.contains_phi:
        return Decision(False, "sales_call_contains_phi")
    if request.on_dnc:
        return Decision(False, "destination_is_suppressed")
    if request.daily_limit < 1 or request.daily_count >= request.daily_limit:
        return Decision(False, "daily_limit_reached")
    return None


def self_call_gate(request: CallRequest) -> Decision:
    if not request.self_calls_enabled:
        return Decision(False, "self_calls_disabled")
    if request.destination not in set(request.allowed_self_numbers):
        return Decision(False, "self_destination_not_allowlisted")
    return Decision(True, "self_call_allowed")


def live_call_gate(request: CallRequest) -> Decision:
    if not request.calls_enabled:
        return Decision(False, "global_sales_calls_disabled")
    if not request.live_calls_enabled:
        return Decision(False, "live_sales_calls_disabled")
    if request.ai_cold_call_policy != "approved":
        return Decision(False, "ai_cold_call_policy_not_approved")
    if not request.disclosure_enabled:
        return Decision(False, "ai_disclosure_missing")
    return Decision(True, "live_call_policy_satisfied")
