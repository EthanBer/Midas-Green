from flask import Flask
from flask_cors import CORS
from config import Config

def start_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    from routes import routes
    app.register_blueprint(routes, url_prefix="/")

    return app


if __name__ == '__main__':
    app = start_app()
    app.run(debug=True)