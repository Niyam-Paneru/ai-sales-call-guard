from __future__ import annotations

from .gates import hard_gate, live_call_gate, self_call_gate
from .models import CallRequest, Decision


def decide(request: CallRequest) -> Decision:
    blocked = hard_gate(request)
    if blocked is not None:
        return blocked

    if request.mode == "self_call":
        return self_call_gate(request)

    if request.mode == "live_prospect":
        return live_call_gate(request)

    return Decision(False, "unknown_call_mode")
