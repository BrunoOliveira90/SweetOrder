from flask import Flask
from flask_bootstrap import Bootstrap
from app.routes import init_routes
from app.models import initialize_db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    Bootstrap(app)
    initialize_db()

    from app.routes import init_routes
    init_routes(app)

    return app