from flask import Flask
from flask_bootstrap import Bootstrap

def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    from app.routes import init_routes
    init_routes(app)

    return app