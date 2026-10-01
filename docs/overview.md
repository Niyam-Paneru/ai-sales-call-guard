# Design overview

This repository is deliberately a policy layer rather than a provider integration.

The flow is intentionally simple:

1. build a request object;
2. apply universal blocks;
3. route into the appropriate mode-specific gate;
4. return one explicit allow/deny decision.

Universal blocks run first so later logic cannot override them.

The public code is a sanitized slice of a larger private system. Provider-specific transport and operational data are intentionally omitted.
