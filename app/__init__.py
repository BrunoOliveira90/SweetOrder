from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
#bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sweetorder.db'
    db.init_app(app)
    #bcrypt.init_app(app)
    login_manager.init_app(app)
    
    from app.models import initialize_db
    initialize_db(app)

    from app.routes import init_routes
    init_routes(app)

    return app
