import os
import unittest
from unittest.mock import patch

from app import create_app


class CreateAppSecretKeyTests(unittest.TestCase):
    def test_raises_when_secret_missing_in_production(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(RuntimeError):
                create_app(debug_mode=False, secret_key="", load_env=False)

    def test_uses_secret_from_environment(self):
        env_vars = {"SECRET_KEY": "super-secret-value"}

        with patch.dict(os.environ, env_vars, clear=True):
            app = create_app(debug_mode=False, load_env=False)

        self.assertEqual(app.secret_key, "super-secret-value")
        self.assertEqual(app.config["SECRET_KEY"], "super-secret-value")
        self.assertFalse(app.config["DEBUG"])

    def test_generates_secret_in_debug_and_logs_warning(self):
        env_vars = {"FLASK_DEBUG": "true"}

        with patch.dict(os.environ, env_vars, clear=True):
            with self.assertLogs("app", level="WARNING") as captured_logs:
                app = create_app(debug_mode=True, secret_key="", load_env=False)

        self.assertTrue(app.config["DEBUG"])
        self.assertTrue(app.secret_key)
        self.assertIn("SECRET_KEY not set", captured_logs.output[0])


if __name__ == "__main__":
    unittest.main()
