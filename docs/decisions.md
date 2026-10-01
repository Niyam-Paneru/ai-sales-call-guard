# Decisions

## Universal blocks run first

Some conditions are stronger than campaign or mode logic and should end evaluation immediately.

## Self-test and external-call modes are separate

Permission for one does not imply permission for the other.

## Unknown mode means deny

A typo should not discover a permissive fallback.

## Decisions carry reasons

Every refusal names the rule that blocked it so the caller can fix configuration instead of guessing.

> “Probably okay” is not a policy result.
