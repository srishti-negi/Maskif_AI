from flask import Flask 
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = LoginManager(app)

from app import models, routes

@login_manager.user_loader
def load_user(userid):
    return User.get(int(userid))
