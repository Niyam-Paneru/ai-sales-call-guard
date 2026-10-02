# AI Sales Call Guard

A default-deny **pre-transport policy layer** that decides whether a self-test call or an external prospect call is eligible to proceed.

This repository never places a call. It contains no provider SDK, credentials, contact list, or dialing transport; its job ends at `Decision(allowed, reason)`.

```mermaid
flowchart TD
    R["CallRequest"] --> H{"Universal hard gates clear?<br/>PHI · suppression · daily cap"}
    H -- "no" --> HD["DENY<br/>hard-gate reason"]
    H -- "yes" --> M{"request.mode"}

    M -- "self_call" --> S{"Self calls enabled<br/>and destination allowlisted?"}
    S -- "no" --> SD["DENY<br/>self-mode reason"]
    S -- "yes" --> SA["ALLOW<br/>self_call_allowed"]

    M -- "live_prospect" --> L{"Global + live enabled,<br/>policy approved, disclosure on?"}
    L -- "no" --> LD["DENY<br/>live-mode reason"]
    L -- "yes" --> LA["ALLOW<br/>live_call_policy_satisfied"]

    M -- "other" --> U["DENY<br/>unknown_call_mode"]
```

The order matters: mode-specific logic is unreachable until the universal gates pass. Unknown modes do not get improvisation privileges; they get `unknown_call_mode`.

## Decision paths

| Path | Required state | Allow reason | Representative deny reasons |
|---|---|---|---|
| Universal gates | no PHI flag, destination not suppressed, below daily limit | continue to mode dispatch | `sales_call_contains_phi`, `destination_is_suppressed`, `daily_limit_reached` |
| `self_call` | `self_calls_enabled` and destination in `allowed_self_numbers` | `self_call_allowed` | `self_calls_disabled`, `self_destination_not_allowlisted` |
| `live_prospect` | `calls_enabled`, `live_calls_enabled`, policy input equals `approved`, disclosure enabled | `live_call_policy_satisfied` | `global_sales_calls_disabled`, `live_sales_calls_disabled`, `ai_cold_call_policy_not_approved`, `ai_disclosure_missing` |
| any other mode | none | — | `unknown_call_mode` |

`ai_cold_call_policy="approved"` is an **application policy input**. It is not evidence of legal compliance, consent, or permission to call in any jurisdiction.

## Request integrity

`CallRequest` rejects blank destinations and invalid counters. It also snapshots the caller-provided self-call allowlist into a `frozenset`, so mutating the original set later cannot widen an already-created request. Those invariants stay in prose and tests rather than turning the decision diagram into a wiring closet.

## Boundary

This module owns only call-mode eligibility **before transport**. Generic agent/tool authorization happens earlier; provider dialing and realtime media behavior happen later. None of those surrounding layers are implemented here.

## Read the implementation

- [`src/sales_call_guard/models.py`](src/sales_call_guard/models.py) — validated request/decision types and immutable allowlist snapshot.
- [`src/sales_call_guard/gates.py`](src/sales_call_guard/gates.py) — universal, self-test, and external-call checks.
- [`src/sales_call_guard/policy.py`](src/sales_call_guard/policy.py) — hard-gate-first dispatch and default deny.
- [`tests/`](tests/) — behavior checks for hard gates, request integrity, both modes, and unknown-mode denial.

Verification commands and what they prove: [`docs/verification.md`](docs/verification.md).

## Limits and provenance

This is a sanitized policy slice from guarded outbound-call experiments in private DentSignal work. Provider transport, credentials, real contact data, campaign data, and operational call flows are intentionally excluded.

See [`PROVENANCE.md`](PROVENANCE.md) for what was preserved and [`SECURITY.md`](SECURITY.md) for the public safety boundary.
