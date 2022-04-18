from calendar import monthrange
from datetime import datetime

from dateutil.utils import today
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError

from app.models import Month_plans


class MonthPlanForm(
	FlaskForm):  # todo rethink the validation because it prevents from editing the month plan| dynamic validation
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

