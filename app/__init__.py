from flask import Flask

def create_app():
    app = Flask(__name__)

    # Enable debug mode
    app.config['DEBUG'] = True
    # Replace 'your_secret_key_here' with an actual secret key
    app.secret_key = 'J!T$2XSizvQSV4w!'

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app