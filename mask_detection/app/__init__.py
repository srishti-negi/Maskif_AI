from flask import Flask 
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)
app.config.from_object(Config)
mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
loginmanager = LoginManager(app)
loginmanager.login_view = 'login'

from app import models, routes

