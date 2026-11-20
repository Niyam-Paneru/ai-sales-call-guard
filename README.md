# AI Sales Call Guard

This is a sales-call project whose proudest feature is **not calling people**.

Not terribly exciting for the robot's sales targets. Excellent for anyone who put a number on the suppression list.

The Python module sits *before* the dialer. Give it a `CallRequest`, and it returns a decision and reason. It doesn't make calls. It decides whether a caller should even be allowed to try.

## The robot's very short guest list

Every request is checked first for sensitive-data flags, suppressed destinations, and the daily cap. **Any failure stops the request**, regardless of mode.

| Mode | Conditions |
| --- | --- |
| self_call | Self-tests enabled; exact destination on the self-call allowlist |
| live_prospect | Global and live switches enabled; application-policy approval and disclosure enabled |
| Anything else | Reject with unknown_call_mode |

The self-call allowlist is copied into an immutable set. Editing the original list afterwards doesn't turn an unauthorized number into “oh, that one was always there.”

Approval cannot bypass suppression or daily limits. An application setting named `approved` is **not legal consent or compliance certification**.

Follow [models](src/sales_call_guard/models.py), [hard/mode gates](src/sales_call_guard/gates.py), [dispatch](src/sales_call_guard/policy.py), [tests](tests/), and the [rejection cases](docs/verification.md).

## No dial tone here

There is no telephony provider, number list, contact database, campaign workflow, or outbound calling. The module supplies a decision contract; any real application must implement additional policy, consent, and transport checks.

You can make the caller persuasive later. First make sure it knows how to take no for an answer. [Security](SECURITY.md) · [provenance](PROVENANCE.md).
