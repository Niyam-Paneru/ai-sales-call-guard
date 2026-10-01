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
