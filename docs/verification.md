# Verification

These commands verify the public policy slice; they do not place a call or prove legal compliance.

## Behavior and syntax

Linux/macOS/CI:

```bash
python -m compileall -q src
PYTHONPATH=src python -m unittest discover -s tests
```

Windows PowerShell:

```powershell
python -m compileall -q src
$env:PYTHONPATH = "src"
python -m unittest discover -s tests
```

The behavior tests cover:

- universal PHI, suppression, and daily-cap hard gates;
- default deny for unknown modes;
- self-call enablement and allowlisting;
- immutable snapshotting of the caller-owned allowlist;
- request validation for blank destinations and invalid counters;
- every live-prospect gate and the all-gates-pass allow path.

## CI boundary

[`.circleci/config.yml`](../.circleci/config.yml) runs source compilation, the unittest suite, and public-proof file checks.

A CI configuration is not evidence that a particular remote commit passed. Inspect the current PR/commit checks before making that claim.
