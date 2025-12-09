import os
import secrets

from dotenv import load_dotenv
from flask import Flask


def _get_bool_env(var_name: str, default: bool = False) -> bool:
    """Return a boolean value for the given environment variable."""

    value = os.getenv(var_name)
    if value is None:
        return default

    return value.strip().lower() in {"true", "1", "t", "yes", "y", "on"}


def create_app(
    debug_mode: bool | None = None,
    secret_key: str | None = None,
    load_env: bool = True,
):
    """Create and configure the Flask application."""

    # Load environment variables from .env file
    if load_env:
        load_dotenv()

    app = Flask(__name__)

    if debug_mode is None:
        debug_mode = _get_bool_env("FLASK_DEBUG", _get_bool_env("DEBUG", False))

    app.config["DEBUG"] = debug_mode
    app.debug = debug_mode

    if secret_key is None:
        secret_key = os.getenv("SECRET_KEY")

    if not secret_key:
        if debug_mode:
            secret_key = secrets.token_hex(32)
            app.logger.warning(
                "SECRET_KEY not set; generated a temporary key for development. "
                "Set SECRET_KEY in your environment for consistent sessions."
            )
        else:
            raise RuntimeError(
                "SECRET_KEY is required when running in production. "
                "Set the SECRET_KEY environment variable."
            )

    app.config["SECRET_KEY"] = secret_key
    app.secret_key = secret_key

    from .routes import main_bp

    app.register_blueprint(main_bp)

    return app


# Đảm bảo rằng app được đặt tên là 'app'
app = create_app()
