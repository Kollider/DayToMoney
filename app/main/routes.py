from calendar import monthrange
from datetime import datetime, date
from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import current_user

from app.helper.daily_plan_table import delta_flow_test
from app.models import Spendings, Month_plans

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home", methods=['GET', 'POST'])
def home():
	if not current_user.is_authenticated:
		flash('Please login to use Day to Money', 'success')
		return redirect(url_for('main.about'))
	today_date = date.today()
	day_spending = Spendings.query.filter_by(user_id=current_user.id).filter(Spendings.day == today_date).order_by(
		Spendings.id.desc()).all()

	start_checkpoint = datetime.strptime('01.' + f'{today_date.month}.{today_date.year}', '%d.%m.%Y').date()
	next_checkpoint = datetime.strptime(
		f'{monthrange(today_date.year, today_date.month)[1]}.{today_date.month}.{today_date.year}', '%d.%m.%Y').date()

	bla = Spendings.query.filter_by(user_id=current_user.id).filter(Spendings.day >= start_checkpoint,
																	Spendings.day <= next_checkpoint)

	month_plan_delta = Month_plans.query.filter_by(user_id=current_user.id).filter(
		Month_plans.month >= start_checkpoint, Month_plans.month <= next_checkpoint).first()

	if not month_plan_delta:  # If user doesn't have a month plan this prevents error
		flash("You don't have a plan for current month. Please add plan", 'danger')
		return redirect(url_for('month_plans.show_all_months'))

	a = delta_flow_test(start_checkpoint, next_checkpoint, bla, month_plan_delta.money_for_day)
	dynamic_mid = a[f'{today_date.strftime("%d.%m")}']['dynamic_mid']
	day_sum = a[f'{today_date.strftime("%d.%m")}']['day_result']
	mid_sum_delta = round(dynamic_mid + day_sum, 2)

	return render_template('home.html', day_spending=day_spending, dynamic_mid=dynamic_mid, day_sum=day_sum,
						   today_date=today_date, mid_sum_delta=mid_sum_delta)


@main.route('/about')
def about():
	return render_template('main/about.html')
