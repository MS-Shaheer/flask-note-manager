from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

from .views import views
from .auth import auth

from .models import User, Note, db


DB_NAME = 'database.db'

def createApp():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'shamoil18babar56'
    app.config['SQLALCHEMY'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    createDatabase(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def loadUser(id):
        return User.query.get(int(id))

    return app

def createDatabase(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Database Created !!!')
