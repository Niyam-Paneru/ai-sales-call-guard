# AI Sales Call Guard

The most important feature of an automated caller might be its ability to **not call**.

This Python module sits *before* call transport. Give it a CallRequest and it returns a decision and reason. It cannot place a phone call. That's a feature, not an embarrassing omission.

## Who gets past the off switch?

Every request is checked first for sensitive-data flags, suppressed destinations, and the daily cap. **Any failure stops the request**, regardless of mode.

| Mode | Conditions |
| --- | --- |
| self_call | Self-tests enabled; exact destination on the self-call allowlist |
| live_prospect | Global and live switches enabled; application-policy approval and disclosure enabled |
| Anything else | Reject with unknown_call_mode |

The self-call allowlist is copied into an immutable set. Editing the original list afterwards doesn't turn an unauthorized number into “oh, that one was always there.”

Approval is not a backstage pass around suppression or daily limits. And a third-party application setting named “approved” is **not legal consent or compliance certification** — naming a Boolean doesn't make a regulator appear.

Follow [models](src/sales_call_guard/models.py), [hard/mode gates](src/sales_call_guard/gates.py), [dispatch](src/sales_call_guard/policy.py), [tests](tests/), and the [rejection cases](docs/verification.md).

## No dial tone here

There is no telephony provider, number list, contact database, campaign workflow, or outbound calling. The module supplies a decision contract; any real application must implement additional policy, consent, and transport checks.

A good off switch should be deeply boring. Nobody should have to write an incident report titled “the chatbot was feeling persuasive.” [Security](SECURITY.md) · [provenance](PROVENANCE.md).
