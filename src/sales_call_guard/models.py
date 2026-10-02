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

    def __post_init__(self) -> None:
        if not self.destination.strip():
            raise ValueError("destination_required")
        if self.daily_count < 0:
            raise ValueError("daily_count_must_be_non_negative")
        if self.daily_limit < 0:
            raise ValueError("daily_limit_must_be_non_negative")

        # A frozen dataclass is only meaningfully immutable if nested inputs are
        # snapshotted too. Do not retain a caller-owned mutable set.
        object.__setattr__(self, "allowed_self_numbers", frozenset(self.allowed_self_numbers))


@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str
