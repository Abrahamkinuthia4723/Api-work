from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes import report_bp
    app.register_blueprint(report_bp, url_prefix='/protectedmemory')

    return app
