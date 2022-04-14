from calendar import monthrange

from dateutil.utils import today
from datetime import datetime
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, BooleanField, SelectField, PasswordField
from wtforms.fields.html5 import DateField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from .models import Users, Month_plans


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[
		DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_email(self, email):
		user = Users.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError(
				'That email is taken. Please choose a different one.')

	def validate_username(self, username):
		user = Users.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError(
				'That username is taken. Please choose a different one.')


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class SpendingForm(FlaskForm):
	day = DateField('Day', validators=[DataRequired()], default=today)
	name_of_item = StringField('Name of item', validators=[DataRequired()])
	# todo possible two fields: regular text and select from database - group by name and count occurencies and sort
	#  by that number#todo autocomplete when possible
	quantity = FloatField('Quantity', validators=[DataRequired()])
	quantity_type = SelectField('Quantity type', choices=['л', 'мл', 'кг', 'г', 'шт'])
	spending_amount = DecimalField('Spending amount', validators=[DataRequired()])
	submit = SubmitField('Send')


class MonthPlanForm(FlaskForm): #todo rethink the validation because it prevents from editing the month plan| dynamic validation
	month = DateField('Month', validators=[DataRequired()], default=today)
	income = FloatField('Income', validators=[DataRequired()])  # todo check if DecimalField on phone is more accurate
	submit = SubmitField('Add')

	def validate_month(self, month):
		date_from_form = month.data
		if date_from_form:
			comparable_date_start = datetime.strptime('01.' + f'{date_from_form.month}.{date_from_form.year}',
													  '%d.%m.%Y').date()
			comparable_date_end = datetime.strptime(
				f'{monthrange(date_from_form.year, date_from_form.month)[1]}.{date_from_form.month}.{date_from_form.year}',
				'%d.%m.%Y').date()
			month_date = Month_plans.query.filter_by(user_id=current_user.id).filter(
				Month_plans.month >= comparable_date_start, Month_plans.month <= comparable_date_end).first()
			if month_date:
				raise ValidationError(
					'You already have a plan for this month')


class MonthTypeForm(FlaskForm):
	name_of_type = StringField('Name of type')
	amount_choice = SelectField('Type of amount', choices=[('percent', '%'), ('money', '₴')], validate_choice=False)
	amount = FloatField('Amount')
	is_default = BooleanField('Default')
	is_everyday = BooleanField('Every day')
	# month_plan=IntegerField('Month plan')
	submit = SubmitField('Add')
