from dateutil.utils import today
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.fields.html5 import DateField, DecimalField
from wtforms.validators import DataRequired


class SpendingForm(FlaskForm):
	day = DateField('Day', validators=[DataRequired()], default=today)
	name_of_item = StringField('Name of item', validators=[DataRequired()])
	# todo possible two fields: regular text and select from database - group by name and count occurencies and sort
	#  by that number#todo autocomplete when possible
	quantity = FloatField('Quantity', validators=[DataRequired()])
	quantity_type = SelectField('Quantity type', choices=['л', 'мл', 'кг', 'г', 'шт'])
	spending_amount = DecimalField('Spending amount', validators=[DataRequired()])
	submit = SubmitField('Add')
