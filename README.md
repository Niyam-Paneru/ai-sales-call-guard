# AI Sales Call Guard

**A robot with a dial tone should have more rules than a teenager with a borrowed car.**

This is the public policy slice from DentSignal's outbound AI-call experiments. It does **not** place calls. It decides whether a call attempt is even eligible to exist.

![Call policy architecture](docs/workflow.svg)

## What the repo is actually about

The interesting problem is not “how do I call a provider API?”

It is:

- should this request be blocked before any provider sees it?
- is this only a self-test, or a real external call?
- is the destination suppressed?
- did the request cross a privacy boundary?
- are the right switches enabled?
- is the required disclosure gate present?
- has the daily limit already been reached?

The code is split into request models, universal hard gates, mode-specific gates, and the final policy dispatcher.

## Repo map

| Area | Responsibility |
|---|---|
| `models.py` | request + decision types |
| `gates.py` | universal, self-test, and live-call checks |
| `policy.py` | final default-deny routing |
| `tests/` | hard-gate and mode-gate behavior |

This repository deliberately leaves out provider SDKs, phone credentials, contact lists, and automated outreach.

The private system contains the larger operational context and provider-specific plumbing.

Want the guardrails without the sales pitch? Read the [invariants](docs/invariants.md), [failure modes](docs/failure-modes.md), [design decisions](docs/decisions.md), and [provenance](PROVENANCE.md).

> A dial tone is not a governance framework.
