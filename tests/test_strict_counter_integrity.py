import unittest

from sales_call_guard.models import CallRequest
from sales_call_guard.policy import decide


class StrictCounterTests(unittest.TestCase):
    def test_invalid_counts_never_enter_a_call_decision(self):
        for invalid in (float("nan"), float("inf"), float("-inf"), 0.5, True, "0", None):
            with self.subTest(value=repr(invalid)):
                with self.assertRaisesRegex(
                    ValueError, "daily_count_must_be_non_negative_integer"
                ):
                    CallRequest(mode="self_call", destination="+15550000001", daily_count=invalid)

    def test_invalid_limits_cannot_bypass_the_daily_quota(self):
        for invalid in (float("nan"), float("inf"), float("-inf"), 1.5, True, "1", None):
            with self.subTest(value=repr(invalid)):
                with self.assertRaisesRegex(
                    ValueError, "daily_limit_must_be_non_negative_integer"
                ):
                    CallRequest(mode="self_call", destination="+15550000001", daily_limit=invalid)

    def test_quota_remains_hard_for_valid_integral_counters(self):
        request = CallRequest(
            mode="self_call",
            destination="+15550000001",
            self_calls_enabled=True,
            allowed_self_numbers={"+15550000001"},
            daily_count=2,
            daily_limit=2,
        )
        self.assertFalse(decide(request).allowed)
        self.assertEqual(decide(request).reason, "daily_limit_reached")

    def test_unchanged_valid_zero_and_positive_counters(self):
        request = CallRequest(
            mode="self_call",
            destination="+15550000001",
            self_calls_enabled=True,
            allowed_self_numbers={"+15550000001"},
            daily_count=0,
            daily_limit=1,
        )
        self.assertTrue(decide(request).allowed)


if __name__ == "__main__":
    unittest.main()
