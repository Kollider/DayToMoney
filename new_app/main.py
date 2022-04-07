from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

website = Flask(__name__)
website.config['SECRET_KEY'] = '2d00df46ce74700f039ebf42idjfhijdjjc861b955121e75a765d1262b0db534994e51c76'
website.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(website)
bcrypt = Bcrypt(website)
login_manager = LoginManager(website)

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

import routes
from new_app.models import Anonymous

login_manager.anonymous_user = Anonymous
