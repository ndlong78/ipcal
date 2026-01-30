import os
import re
import unittest

from app import create_app


class RouteValidationTests(unittest.TestCase):
    def setUp(self):
        os.environ.setdefault('SECRET_KEY', 'test-secret')
        self.app = create_app()
        self.app.testing = True
        self.app.config["RATE_LIMIT_DISABLED"] = True
        self.client = self.app.test_client()

    def _get_csrf_token(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        match = re.search(r'name="csrf_token" value="([^"]+)"', response.get_data(as_text=True))
        self.assertIsNotNone(match)
        return match.group(1)

    def test_invalid_ip_characters(self):
        csrf_token = self._get_csrf_token()
        response = self.client.post(
            '/calculate',
            data={'ip-address': '192.168.1.1!', 'network': '24', 'csrf_token': csrf_token},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"contains invalid characters", response.data)

    def test_invalid_ipv4_netmask_range(self):
        csrf_token = self._get_csrf_token()
        response = self.client.post(
            '/calculate',
            data={'ip-address': '192.168.1.1', 'network': '300.0.0.0', 'csrf_token': csrf_token},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"octets between 0 and 255", response.data)

    def test_ipv4_cidr_boundary_zero(self):
        csrf_token = self._get_csrf_token()
        response = self.client.post(
            '/calculate',
            data={'ip-address': '8.8.8.8', 'network': '0', 'csrf_token': csrf_token},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<strong>CIDR:</strong> 0", response.data)

    def test_ipv4_cidr_boundary_32(self):
        csrf_token = self._get_csrf_token()
        response = self.client.post(
            '/calculate',
            data={'ip-address': '1.1.1.1', 'network': '32', 'csrf_token': csrf_token},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<strong>CIDR:</strong> 32", response.data)

    def test_ipv6_cidr_boundary_128(self):
        csrf_token = self._get_csrf_token()
        response = self.client.post(
            '/calculate',
            data={'ip-address': '2001:db8::1', 'network': '128', 'csrf_token': csrf_token},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<strong>CIDR:</strong> 128", response.data)


if __name__ == '__main__':
    unittest.main()
