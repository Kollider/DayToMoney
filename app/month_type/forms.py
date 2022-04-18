from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, BooleanField, SubmitField


class MonthTypeForm(FlaskForm):
	name_of_type = StringField('Name of type')
	amount_choice = SelectField('Type of amount', choices=[('percent', '%'), ('money', '₴')], validate_choice=False)
	amount = FloatField('Amount')
	is_default = BooleanField('Default')
	is_everyday = BooleanField('Every day')
	# month_plan=IntegerField('Month plan')
	submit = SubmitField('Add')
