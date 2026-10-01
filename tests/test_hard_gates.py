import unittest

from sales_call_guard.gates import hard_gate
from sales_call_guard.models import CallRequest


class HardGateTests(unittest.TestCase):
    def test_phi_is_rejected_before_mode_specific_logic(self):
        decision = hard_gate(CallRequest(mode="self_call", destination="+15550000001", contains_phi=True))
        self.assertEqual(decision.reason, "sales_call_contains_phi")

    def test_dnc_is_rejected(self):
        decision = hard_gate(CallRequest(mode="live_prospect", destination="+15550000001", on_dnc=True))
        self.assertEqual(decision.reason, "destination_is_suppressed")

    def test_daily_limit_is_rejected(self):
        decision = hard_gate(CallRequest(mode="self_call", destination="+15550000001", daily_count=1, daily_limit=1))
        self.assertEqual(decision.reason, "daily_limit_reached")


if __name__ == "__main__":
    unittest.main()
