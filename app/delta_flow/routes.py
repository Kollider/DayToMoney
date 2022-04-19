from calendar import monthrange
from datetime import datetime
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app.helper.daily_plan_table import delta_flow_test
from app.models import Spendings, Month_plans

delta_flows = Blueprint('delta_flows', __name__)


@delta_flows.route('/planning/daily/delta_flow',
				   methods=['GET', 'POST'])
@login_required
def delta_flow():
	start_checkpoint = datetime.strptime('01.09.2021', '%d.%m.%Y').date()  # todo create form to choose date
	next_checkpoint = datetime.strptime('30.09.2021',
										'%d.%m.%Y').date()  # todo maybe add formFIELDS to choose date with button to redirect to itself on top of the delta

	bla = Spendings.query.filter_by(user_id=current_user.id).filter(Spendings.day >= start_checkpoint,
																	Spendings.day <= next_checkpoint)  # todo change to normal name

	month_plan_id = 1
	month_plan_delta = Month_plans.query.get_or_404(
		month_plan_id)  # todo think about an actual way to obtain month_id| should it be passed or queued in some way?
	b = month_plan_delta.money_for_day

	a = delta_flow_test(start_checkpoint, next_checkpoint, bla, month_plan_delta.money_for_day)

	return render_template('delta_flow.html', delta_flow_results=a,
						   start_checkpoint=start_checkpoint.strftime("%d.%m.%y"),
						   next_checkpoint=next_checkpoint.strftime("%d.%m.%y"),
						   prev_checkpoint=b)  # todo check naming #todo format dates to human-friendly


@delta_flows.route('/planning/daily/delta_flow/test',
				   methods=['GET', 'POST'])
@login_required
def delta_flow_month():
	month_plan_id = request.args.get('month_plan_id')
	month_plan_delta = Month_plans.query.get_or_404(month_plan_id)
	start_checkpoint = datetime.strptime('01.' + f'{month_plan_delta.month.month}.{month_plan_delta.month.year}',
										 '%d.%m.%Y').date()  # todo create form to choose date
	next_checkpoint = datetime.strptime(
		f'{monthrange(month_plan_delta.month.year, month_plan_delta.month.month)[1]}.{month_plan_delta.month.month}.{month_plan_delta.month.year}',
		'%d.%m.%Y').date()  # todo maybe add formFIELDS to choose date with button to redirect to itself on top of the delta
	bla = Spendings.query.filter_by(user_id=current_user.id).filter(Spendings.day >= start_checkpoint,
																	Spendings.day <= next_checkpoint)  # todo change to normal name

	b = month_plan_delta.money_for_day

	a = delta_flow_test(start_checkpoint, next_checkpoint, bla, month_plan_delta.money_for_day)

	return render_template('delta_flow.html', delta_flow_results=a, start_checkpoint=start_checkpoint,
						   next_checkpoint=next_checkpoint,
						   prev_checkpoint=b)  # todo check naming #todo format dates to human-friendly
