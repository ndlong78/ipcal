#Tệp này khởi tạo ứng dụng Flask và đăng ký các blueprint.

from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
