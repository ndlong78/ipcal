import unittest

from app.calculations import (
    calculate_ipv4_network_and_subnet,
    calculate_ipv6_network_and_subnet,
)


class NetworkCalculationEdgeCaseTests(unittest.TestCase):
    def test_ipv4_31_hosts_are_usable(self):
        result = calculate_ipv4_network_and_subnet("192.168.1.10", "31")
        self.assertNotIn("error", result)
        self.assertEqual(result["Network Address"], "192.168.1.10")
        self.assertEqual(result["Broadcast Address"], "192.168.1.11")
        self.assertEqual(result["HostMin"], "192.168.1.10")
        self.assertEqual(result["HostMax"], "192.168.1.11")
        self.assertEqual(result["Total Hosts"], 2)

    def test_ipv4_32_single_host(self):
        result = calculate_ipv4_network_and_subnet("10.0.0.5", "32")
        self.assertNotIn("error", result)
        self.assertEqual(result["Network Address"], "10.0.0.5")
        self.assertEqual(result["Broadcast Address"], "10.0.0.5")
        self.assertEqual(result["HostMin"], "10.0.0.5")
        self.assertEqual(result["HostMax"], "10.0.0.5")
        self.assertEqual(result["Total Hosts"], 1)
        self.assertEqual(result["Wildcard"], "0.0.0.0")

    def test_ipv6_127_usable_pair(self):
        result = calculate_ipv6_network_and_subnet("2001:db8::1", "127")
        self.assertNotIn("error", result)
        self.assertEqual(result["Network Address"], "2001:db8::")
        self.assertEqual(result["Broadcast Address"], "2001:db8::1")
        self.assertEqual(result["HostMin"], "2001:db8::")
        self.assertEqual(result["HostMax"], "2001:db8::1")
        self.assertEqual(result["Total Hosts"], 2)

    def test_ipv6_128_single_address(self):
        result = calculate_ipv6_network_and_subnet("2001:db8::1", "128")
        self.assertNotIn("error", result)
        self.assertEqual(result["Network Address"], "2001:db8::1")
        self.assertEqual(result["Broadcast Address"], "2001:db8::1")
        self.assertEqual(result["HostMin"], "2001:db8::1")
        self.assertEqual(result["HostMax"], "2001:db8::1")
        self.assertEqual(result["Total Hosts"], 1)


if __name__ == "__main__":
    unittest.main()
