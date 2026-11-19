# AI Sales Call Guard

I don't think an AI caller should be able to improvise its way around an off switch.

This Python module sits **before** call transport. Give it a `CallRequest`; it gives you a decision and reason. It does **not** dial anybody. That distinction is doing a lot of work.

### Who gets through?

The universal checks run first: sensitive-data flag, suppressed destination, and daily cap. Failing one of those ends the decision.

Then the mode matters:

| Mode | What has to be true |
| --- | --- |
| `self_call` | Self-tests enabled, destination in the exact self-call allowlist |
| `live_prospect` | Global and live switches on, application-policy input approved, disclosure enabled |
| Anything else | Nope. `unknown_call_mode` |

The supplied self-call list is copied into an immutable set. Changing the caller's original Python set later doesn't silently authorize another number.

This is the sort of feature nobody notices when it works, which is probably what you want from a call-safety gate.

## The call never reaches transport unless both gates agree

The universal checks get first refusal, regardless of mode.

```mermaid
---
config:
  flowchart:
    curve: linear
    nodeSpacing: 28
    rankSpacing: 42
---
flowchart LR
    accTitle: Hard gates: reject before mode dispatch
    accDescr: Decision flow for hard gates: reject before mode dispatch.
    R["CallRequest"] --> H{"Hard gates clear?"}
    H -- No --> D["Deny<br/>Hard-gate reason"]
    H -- Yes --> M["Dispatch mode"]
    classDef input stroke-width:1.5px;
    classDef pass stroke-width:2.5px;
    classDef stop stroke-width:2px,stroke-dasharray:5 3;
    class R,H,M input;
    class D stop;
```

Passing those checks only gets the request as far as its mode-specific policy.

```mermaid
---
config:
  flowchart:
    curve: linear
    nodeSpacing: 28
    rankSpacing: 42
---
flowchart TB
    accTitle: Modes: enablement is specific to the call path
    accDescr: Decision flow for modes: enablement is specific to the call path.
    M{"Mode?"} -- self_call --> S{"Self gates clear?"}
    S -- No --> SD["Deny<br/>Self-mode reason"]
    S -- Yes --> SA["Allow<br/>self_call_allowed"]
    M -- live_prospect --> L{"Live gates clear?"}
    L -- No --> LD["Deny<br/>Live-mode reason"]
    L -- Yes --> LA["Allow<br/>live_call_policy_satisfied"]
    M -- Other --> U["Deny<br/>unknown_call_mode"]
    classDef input stroke-width:1.5px;
    classDef pass stroke-width:2.5px;
    classDef stop stroke-width:2px,stroke-dasharray:5 3;
    class M,S,L input;
    class SA,LA pass;
    class SD,LD,U stop;
```

Look at [models](src/sales_call_guard/models.py), [hard and mode gates](src/sales_call_guard/gates.py), [dispatch](src/sales_call_guard/policy.py), and [tests](tests/). The [verification page](docs/verification.md) lists the exact refusal cases.

**No calls are placed here.** No provider credentials, contact data, or campaign workflow. An application setting called `approved` is **not** legal consent, compliance certification, or permission to call someone. See [SECURITY.md](SECURITY.md) and [PROVENANCE.md](PROVENANCE.md).
