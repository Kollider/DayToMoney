import datetime

from sqlalchemy import true, false

from new_app.main import db


class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)

	spent = db.relationship('Spendings', backref='user_spent', lazy=True)


class Spendings(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	day = db.Column(db.Date, nullable=True, default=datetime.date.today)
	name_of_item = db.Column(db.String(40), nullable=True)
	quantity = db.Column(db.Integer, nullable=True, default=1)
	quantity_type = db.Column(db.String(5), nullable=True, default='it')
	spending_amount = db.Column(db.Float, nullable=True)

	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, default=1)


class Month_plans(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	month = db.Column(db.Date, nullable=true)
	income = db.Column(db.Float, nullable=True, default=0)
	money_for_month = db.Column(db.Float, nullable=True, default=0)
	money_for_day = db.Column(db.Float, nullable=True, default=0)

	list_of_planned_spending = db.relationship('Types_of_month_spend', backref='list_for_month', lazy=True)


class Types_of_month_spend(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name_of_type = db.Column(db.String(40), nullable=True)
	amount_in_percent = db.Column(db.Float, nullable=True)
	amount_in_money = db.Column(db.Float, nullable=True)
	is_default = db.Column(db.Boolean, nullable=True, default=0)
	is_everyday = db.Column(db.Boolean, nullable=True, default=0)

	month_plan = db.Column(db.Integer, db.ForeignKey('month_plans.id'), nullable=True)
