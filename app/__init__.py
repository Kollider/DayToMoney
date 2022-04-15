import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = '2d00df46ce74700f039ebf42idjfhijdjjc861b955121e75a765d1262b0db534994e51c76'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from .routes import *
from .models import Anonymous

login_manager.anonymous_user = Anonymous
