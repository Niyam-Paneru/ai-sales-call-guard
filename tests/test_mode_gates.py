import unittest

from sales_call_guard.gates import live_call_gate, self_call_gate
from sales_call_guard.models import CallRequest


class ModeGateTests(unittest.TestCase):
    def test_self_call_needs_allowlist(self):
        decision = self_call_gate(CallRequest(
            mode="self_call",
            destination="+15550000002",
            self_calls_enabled=True,
            allowed_self_numbers={"+15550000001"},
        ))
        self.assertEqual(decision.reason, "self_destination_not_allowlisted")

    def test_live_call_needs_disclosure(self):
        decision = live_call_gate(CallRequest(
            mode="live_prospect",
            destination="+15550000003",
            calls_enabled=True,
            live_calls_enabled=True,
            ai_cold_call_policy="approved",
        ))
        self.assertEqual(decision.reason, "ai_disclosure_missing")

    def test_live_call_passes_only_when_all_switches_are_on(self):
        decision = live_call_gate(CallRequest(
            mode="live_prospect",
            destination="+15550000003",
            calls_enabled=True,
            live_calls_enabled=True,
            ai_cold_call_policy="approved",
            disclosure_enabled=True,
        ))
        self.assertTrue(decision.allowed)


if __name__ == "__main__":
    unittest.main()
