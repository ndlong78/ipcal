from flask import Flask

def create_app():
    app = Flask(__name__)

    # Bật chế độ debug
    app.config['DEBUG'] = True
    app.secret_key = 'your_secret_key_here'

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app