import datetime

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, AnonymousUserMixin

from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))


class Anonymous(AnonymousUserMixin):
	def __init__(self):
		self.username = 'Guest'
		self.status = False


class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	status = db.Column(db.Boolean, default=False)

	spent = db.relationship('Spendings', backref='user_spent', lazy=True)
	plans = db.relationship('Month_plans', backref='plans', lazy=True)

	def get_reset_token(self, expires_sec=600):
		serial_token = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return serial_token.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		serial_token = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = serial_token.loads(token)['user_id']
		except:
			return None
		return Users.query.get_or_404(user_id)



class Spendings(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	day = db.Column(db.Date, nullable=True, default=datetime.date.today)
	name_of_item = db.Column(db.String(40), nullable=True)
	quantity = db.Column(db.Integer, nullable=True, default=1)
	quantity_type = db.Column(db.String(5), nullable=True, default='it')
	spending_amount = db.Column(db.Float, nullable=True)

	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, default=1)  # todo change id


class Month_plans(db.Model):  # todo think about cascading delete with sqlalchemy
	id = db.Column(db.Integer, primary_key=True)
	month = db.Column(db.Date, nullable=True)
	income = db.Column(db.Float, nullable=True, default=0)
	money_for_month = db.Column(db.Float, nullable=True, default=0)
	money_for_day = db.Column(db.Float, nullable=True, default=0)

	list_of_planned_spending = db.relationship('Types_of_month_spend', backref='list_for_month', lazy=True)

	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, default=1)  # todo change id


class Types_of_month_spend(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name_of_type = db.Column(db.String(40), nullable=True)
	amount_in_percent = db.Column(db.Float, nullable=True)
	amount_in_money = db.Column(db.Float, nullable=True)
	is_default = db.Column(db.Boolean, nullable=True, default=0)
	is_everyday = db.Column(db.Boolean, nullable=True, default=0)

	month_plan = db.Column(db.Integer, db.ForeignKey('month_plans.id'), nullable=True)
