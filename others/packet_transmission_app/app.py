# Check and force transmission to the server packet.


from flask import Flask
from teams_server.routes import teams_server_bp

app = Flask(__name__)

app.register_blueprint(teams_server_bp, url_prefix="/teams_server")

@app.route("/")
def index():
    return {"message": "Teams Server API"}, 200

if __name__ == "__main__":
    app.run(debug=True)
