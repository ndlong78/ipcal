from flask import Flask

def create_app():
    app = Flask(__name__)

    # Bật chế độ debug
    app.config['DEBUG'] = True
    # Thay thế 'your_secret_key_here' bằng một chuỗi bí mật thực sự
    app.secret_key = 'J!T$2XSizvQSV4w!'

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app