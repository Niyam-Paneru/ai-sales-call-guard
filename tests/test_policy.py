import unittest

from sales_call_guard.policy import CallRequest, decide


class SalesCallGuardTests(unittest.TestCase):
    def test_unknown_mode_denies(self):
        d = decide(CallRequest(mode="mystery", destination="+1"))
        self.assertFalse(d.allowed)
        self.assertEqual(d.reason, "unknown_call_mode")

    def test_phi_denies_everything(self):
        d = decide(CallRequest(
            mode="self_call",
            destination="+15550000001",
            self_calls_enabled=True,
            allowed_self_numbers={"+15550000001"},
            contains_phi=True,
        ))
        self.assertEqual(d.reason, "sales_call_contains_phi")

    def test_dnc_denies(self):
        d = decide(CallRequest(mode="live_prospect", destination="+1", on_dnc=True))
        self.assertEqual(d.reason, "destination_is_suppressed")

    def test_self_call_requires_switch(self):
        d = decide(CallRequest(
            mode="self_call",
            destination="+15550000001",
            allowed_self_numbers={"+15550000001"},
        ))
        self.assertEqual(d.reason, "self_calls_disabled")

    def test_self_call_requires_allowlist(self):
        d = decide(CallRequest(
            mode="self_call",
            destination="+15550000002",
            self_calls_enabled=True,
            allowed_self_numbers={"+15550000001"},
        ))
        self.assertEqual(d.reason, "self_destination_not_allowlisted")

    def test_self_call_can_pass(self):
        d = decide(CallRequest(
            mode="self_call",
            destination="+15550000001",
            self_calls_enabled=True,
            allowed_self_numbers={"+15550000001"},
        ))
        self.assertTrue(d.allowed)
        self.assertEqual(d.reason, "self_call_allowed")

    def test_daily_limit_is_hard(self):
        d = decide(CallRequest(
            mode="self_call",
            destination="+15550000001",
            self_calls_enabled=True,
            allowed_self_numbers={"+15550000001"},
            daily_count=1,
            daily_limit=1,
        ))
        self.assertEqual(d.reason, "daily_limit_reached")

    def test_live_call_requires_global_switch(self):
        d = decide(CallRequest(
            mode="live_prospect",
            destination="+15550000003",
            live_calls_enabled=True,
            ai_cold_call_policy="approved",
            disclosure_enabled=True,
        ))
        self.assertEqual(d.reason, "global_sales_calls_disabled")

    def test_live_call_requires_live_switch(self):
        d = decide(CallRequest(
            mode="live_prospect",
            destination="+15550000003",
            calls_enabled=True,
            ai_cold_call_policy="approved",
            disclosure_enabled=True,
        ))
        self.assertEqual(d.reason, "live_sales_calls_disabled")

    def test_live_call_requires_approved_policy(self):
        d = decide(CallRequest(
            mode="live_prospect",
            destination="+15550000003",
            calls_enabled=True,
            live_calls_enabled=True,
            disclosure_enabled=True,
        ))
        self.assertEqual(d.reason, "ai_cold_call_policy_not_approved")

    def test_live_call_requires_disclosure(self):
        d = decide(CallRequest(
            mode="live_prospect",
            destination="+15550000003",
            calls_enabled=True,
            live_calls_enabled=True,
            ai_cold_call_policy="approved",
        ))
        self.assertEqual(d.reason, "ai_disclosure_missing")

    def test_live_call_can_pass_only_all_gates(self):
        d = decide(CallRequest(
            mode="live_prospect",
            destination="+15550000003",
            calls_enabled=True,
            live_calls_enabled=True,
            ai_cold_call_policy="approved",
            disclosure_enabled=True,
        ))
        self.assertTrue(d.allowed)
        self.assertEqual(d.reason, "live_call_policy_satisfied")


if __name__ == "__main__":
    unittest.main()
