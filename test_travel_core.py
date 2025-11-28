import math
import unittest

from travel_core import activate_travel_mode, get_fx_rate


class TestFxRateLookup(unittest.TestCase):
    def test_direct_rate_lookup(self):
        self.assertEqual(get_fx_rate("EUR", "HUF"), 390.0)

    def test_inverse_rate_lookup(self):
        # Only EUR->GBP is stored; GBP->EUR should be derived via reciprocal
        rate = get_fx_rate("GBP", "EUR")
        self.assertIsNotNone(rate)
        self.assertAlmostEqual(rate, 1 / 0.86, places=6)

    def test_same_currency_rate(self):
        self.assertEqual(get_fx_rate("USD", "USD"), 1.0)


class TestActivateTravelMode(unittest.TestCase):
    def test_travel_mode_uses_inverse_rate(self):
        # Local currency resolves to EUR; only EUR->GBP is stored so GBP->EUR
        # should be derived via reciprocal.
        state = activate_travel_mode("user-1", "EE", "GBP")
        self.assertTrue(math.isclose(state.fx_rate, 1 / 0.86))


if __name__ == "__main__":
    unittest.main()
