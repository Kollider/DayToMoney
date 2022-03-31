from dateutil.utils import today
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, BooleanField, SelectField
from wtforms.fields.html5 import DateField, DecimalField, IntegerField
from wtforms.validators import DataRequired


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
	income = FloatField('Income', validators=[DataRequired()])
	"""money_for_month=FloatField('Money for month')
	money_for_day=FloatField('Money for day')"""

	submit = SubmitField('Send')


class MonthTypeForm(FlaskForm):
	name_of_type = StringField('Name of type')
	amount_choice = SelectField('Type of amount', choices=[('percent', '%'), ('money', 'UAH')],validate_choice=False)
	amount = FloatField('Amount')
	is_default = BooleanField('Default')
	is_everyday = BooleanField('Every day')
	# month_plan=IntegerField('Month plan')

	submit = SubmitField('Send')
