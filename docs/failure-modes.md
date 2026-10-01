# Failure modes

## Suppressed destination
A destination appears on the suppression list. Response: hard deny before mode-specific logic.

## Privacy boundary crossed
The request carries prohibited personal/health context for the sales path. Response: hard deny.

## Self-test permission is mistaken for external permission
A safe allowlisted test path is treated as proof live calling is enabled. Response: keep capabilities separate.

## Required disclosure gate is absent
The external path is otherwise enabled but disclosure is not. Response: deny.

## Daily cap is reached
The request is valid but the configured limit is exhausted. Response: deny.

## Unknown mode
A typo or new mode bypasses reviewed logic. Response: default deny.
