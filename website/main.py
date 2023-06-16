from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

#importing all external files for runnning of app
def create_app():
    #initialising database
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_mum'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    #importing other python files
    from views import views
    from auth import auth
    from emails import emails

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(emails, url_prefix='/')

    #importing database
    from models import User

    create_database(app)

    #user session management (required initialisation) 
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #referencing user ID
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

#final configuration of database for app
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')
