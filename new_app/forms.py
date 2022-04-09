from dateutil.utils import today
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, BooleanField, SelectField, PasswordField
from wtforms.fields.html5 import DateField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from new_app.models import Users


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
	name_of_item = StringField('Name of item', validators=[
		DataRequired()])  # todo possible two fields: regular text and select from database - group by name and count occurencies and sort by that number#todo autocomplete when possible
	quantity = FloatField('Quantity', validators=[DataRequired()])
	quantity_type = SelectField('Quantity type', choices=['л', 'мл', 'кг', 'г',
														  'шт'])  # StringField('Quantity type', validators=[DataRequired()])
	spending_amount = DecimalField('Spending amount', validators=[DataRequired()])
	submit = SubmitField('Send')


class MonthPlanForm(FlaskForm):
	month = DateField('Month', validators=[DataRequired()], default=today)
	income = FloatField('Income', validators=[DataRequired()]) #todo check if DecimalField on phone is more accurate
	"""money_for_month=FloatField('Money for month')
	money_for_day=FloatField('Money for day')"""

	submit = SubmitField('Send')


class MonthTypeForm(FlaskForm):
	name_of_type = StringField('Name of type')
	amount_choice = SelectField('Type of amount', choices=[('percent', '%'), ('money', '₴')], validate_choice=False)
	amount = FloatField('Amount')
	is_default = BooleanField('Default')
	is_everyday = BooleanField('Every day')
	# month_plan=IntegerField('Month plan')

	submit = SubmitField('Send')
