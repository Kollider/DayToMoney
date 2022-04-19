import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .config import Config

db = SQLAlchemy()
migrate = Migrate(db)
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from .models import Anonymous

login_manager.anonymous_user = Anonymous


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	try:
		db.create_all()
	except Exception as e:
		print(e)
	migrate.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	from .users.routes import users
	from .delta_flow.routes import delta_flows
	from .main.routes import main
	from .month_plan.routes import month_plans
	from .month_type.routes import month_types
	from .spendings.routes import spendings

	from .error.handlers import errors

	app.register_blueprint(users)
	app.register_blueprint(delta_flows)
	app.register_blueprint(main)
	app.register_blueprint(month_plans)
	app.register_blueprint(month_types)
	app.register_blueprint(spendings)

	app.register_blueprint(errors)

	return app


app = create_app()
