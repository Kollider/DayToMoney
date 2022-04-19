from calendar import monthrange

from flask import Blueprint, request, render_template, flash, url_for, redirect
from flask_login import login_required, current_user

from app import db
from app.helper.month_plan_table import plan_to_dict, daily_overall_dict
from app.helper.name_months import months_names
from app.models import Month_plans
from app.month_plan.forms import MonthPlanForm

month_plans = Blueprint('month_plans',__name__)


@month_plans.route('/planning/monthly/months', methods=['GET', 'POST'])
@login_required
def show_all_months():
	page = request.args.get('page', 1, type=int)
	month_plans = Month_plans.query.filter_by(user_id=current_user.id).order_by(Month_plans.month.desc()).paginate(
		page=page, per_page=5)
	return render_template('month_plans/monthplanning.html', month_plans=month_plans, myfunction=months_names)


@month_plans.route('/planning/monthly/new', methods=['GET', 'POST'])
@login_required
def month_plan_new():
	form = MonthPlanForm()
	if form.validate_on_submit():
		monthplan = Month_plans(month=form.month.data,
								income=form.income.data,
								money_for_month=0,
								# todo change 0 to actual value calculated by plan| maybe add more if-coditions to calculate values properly?
								money_for_day=form.income.data,
								user_id=current_user.id)
		db.session.add(monthplan)
		db.session.commit()
		flash('Your month plan has been created', 'success')
		return redirect(url_for('month_plans.show_all_months'))
	return render_template('month_plans/create_new_month_plan.html', title='New Month Plan', form=form, legend='New Month Plan')


@month_plans.route('/planning/monthly/<int:month_plan_id>',
		   methods=['GET', 'POST'])
@login_required
def month_plan_table_test(month_plan_id):
	month_plan = Month_plans.query.get_or_404(month_plan_id)
	days = monthrange(month_plan.month.year, month_plan.month.month)[1]

	return render_template('month_plans/month_plan.html', title=str(month_plan.month.month) + '.' + str(month_plan.month.year),
						   month_plan=month_plan, legend='TEST LEGEND FOR MONTH PLAN',
						   planDictionary=plan_to_dict(month_plan), days=days,
						   monthOverall=daily_overall_dict(plan_to_dict(month_plan), month_plan.income))


@month_plans.route('/planning/monthly/<int:month_plan_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_month_plan(month_plan_id):
	if not current_user.is_authenticated:
		return redirect(url_for('main.about'))
	month_plan = Month_plans.query.get_or_404(month_plan_id)
	db.session.delete(month_plan)
	db.session.commit()
	flash('Month plan deleted successfully', 'success')
	return redirect(url_for('month_plans.show_all_months'))


@month_plans.route('/planning/monthly/<int:month_plan_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_month_plan(month_plan_id):
	if not current_user.is_authenticated:
		return redirect(url_for('main.about'))
	month_plan = Month_plans.query.get_or_404(month_plan_id)
	form = MonthPlanForm()
	if form.validate_on_submit():
		month_plan.month = form.month.data
		month_plan.income = form.income.data
		db.session.commit()
		flash('Month plan has been edited successfully', 'success')
		return redirect(url_for('month_plans.month_plan_table_test', month_plan_id=month_plan.id))
	elif request.method == 'GET':
		form.month.data = month_plan.month
		form.income.data = month_plan.income
	return render_template('month_plans/create_new_month_plan.html', title='Edit Month Plan', legend='Edit Month Plan', form=form)

