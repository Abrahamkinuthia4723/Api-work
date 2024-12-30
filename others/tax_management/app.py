from flask import Flask
from flask_cors import CORS
from routes.server import server_bp
from routes.receipt import receipt_bp
from routes.status import status_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(server_bp, url_prefix='/server')
app.register_blueprint(receipt_bp, url_prefix='/receipt')
app.register_blueprint(status_bp, url_prefix='/status')

if __name__ == "__main__":
    app.run(debug=True)
