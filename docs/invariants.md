# Invariants

1. **Suppressed destinations are denied before mode-specific logic.**
2. **The sales path never accepts prohibited sensitive context.**
3. **Self-test permission does not imply external-call permission.**
4. **Unknown call modes default to deny.**
5. **Required disclosure state is explicit, not assumed from a prompt.**
6. **Daily limits are enforced before transport.**
7. **The policy layer does not place calls itself.**

A provider SDK should never be the first place a risky request learns it was not allowed.
