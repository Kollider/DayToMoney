from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.models import Types_of_month_spend, Users, Month_plans
from app.month_type.forms import MonthTypeForm

month_types = Blueprint('month_types',__name__)


@month_types.route('/planning/monthly/types/all', methods=['GET', 'POST'])
@login_required
def show_all_types():
	page = request.args.get('page', 1, type=int)
	# plans = [plan for plan in Users.query.filter_by(id=current_user.id).first().plans]
	month_types = Types_of_month_spend.query.filter(Types_of_month_spend.month_plan.in_([plan_id.id for plan_id in
																						 [plan for plan in
																						  Users.query.filter_by(
																							  id=current_user.id).first().plans]])).order_by(
		Types_of_month_spend.id.desc()).paginate(page=page, per_page=5)
	return render_template('month_types/month_types_all.html', month_types=month_types)


@month_types.route('/planning/monthly/<int:month_plan_id>/types/new', methods=['GET', 'POST'])
@login_required
def month_type_new(month_plan_id):
	form = MonthTypeForm()
	if form.validate_on_submit():
		month_plan = Month_plans.query.get_or_404(month_plan_id)
		type_income = month_plan.income
		if form.amount_choice.data == 'percent':
			amount_in_percent = form.amount.data
			amount_in_money = type_income * amount_in_percent / 100
		elif form.amount_choice.data == 'money':
			amount_in_money = form.amount.data
			amount_in_percent = amount_in_money / type_income * 100

		monthtype = Types_of_month_spend(name_of_type=form.name_of_type.data,
										 amount_in_percent=round(amount_in_percent, 2),
										 amount_in_money=round(amount_in_money, 2),
										 is_default=form.is_default.data,
										 is_everyday=form.is_everyday.data,
										 month_plan=month_plan_id)

		db.session.add(monthtype)
		if not monthtype.is_everyday:  # currently left amount adds to daily delta flow#todo decide if left amount is adding to month or day
			month_plan.money_for_day -= monthtype.amount_in_money
			month_plan.money_for_month += monthtype.amount_in_money
		db.session.commit()
		flash('Your month plan has been created', 'success')
		return redirect(url_for('month_plans.month_plan_table_test', month_plan_id=month_plan_id))
	return render_template('month_types/create_new_month_type.html', title='New Month Type', form=form, legend='New Month Type')


@month_types.route('/planning/monthly/<int:month_plan_id>/types/<int:month_type_id>')
@login_required
def month_type_single(month_type_id, month_plan_id):
	if not current_user.is_authenticated:
		return redirect(url_for('main.home'))
	month_type_expense = Types_of_month_spend.query.get_or_404(month_type_id)
	bla = month_plan_id
	return render_template('month_types/month_type_single.html', title=month_type_expense.name_of_type,
						   month_type=month_type_expense, month_plan_id=bla)


@month_types.route('/planning/monthly/types/<int:month_type_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_month_type(month_type_id):
	if not current_user.is_authenticated:
		return redirect(url_for('main.home'))
	month_type_expense = Types_of_month_spend.query.get_or_404(month_type_id)
	db.session.delete(month_type_expense)
	db.session.commit()
	flash('Type has been deleted.', 'success')
	return redirect(url_for('main.home'))


@month_types.route('/planning/monthly/<int:month_plan_id>/types/<int:month_type_id>/delete', methods=['GET', 'POST'])
@login_required
def edit_month_type(month_plan_id, month_type_id):
	if not current_user.is_authenticated:
		return redirect(url_for('main.about'))
	month_type_expense = Types_of_month_spend.query.get_or_404(month_type_id)
	form = MonthTypeForm()
	month_plan = Month_plans.query.get_or_404(month_plan_id)
	if form.validate_on_submit():
		type_income = month_plan.income
		if form.amount_choice.data == 'percent':
			amount_in_percent = form.amount.data
			amount_in_money = type_income * amount_in_percent / 100
		elif form.amount_choice.data == 'money':
			amount_in_money = form.amount.data
			amount_in_percent = amount_in_money / type_income * 100

		month_type_expense.name_of_type = form.name_of_type.data
		month_type_expense.amount_in_percent = round(amount_in_percent, 2)
		month_type_expense.amount_in_money = round(amount_in_money, 2)
		month_type_expense.is_default = form.is_default.data
		month_type_expense.is_everyday = form.is_everyday.data
		month_type_expense.month_plan = month_plan_id
		if not month_type_expense.is_everyday:  # currently left amount adds to daily delta flow#todo decide if left amount is adding to month or day
			month_plan.money_for_day -= month_type_expense.amount_in_money
			month_plan.money_for_month += month_type_expense.amount_in_money
		db.session.commit()
		flash('Expense type for month has been edited successfully', 'success')
		return redirect(url_for('month_types.month_type_single', month_type_id=month_type_expense.id, month_plan_id=month_plan.id))
	elif request.method == 'GET':
		form.name_of_type.data = month_type_expense.name_of_type
		form.amount_choice.data = 'money'
		form.amount.data = month_type_expense.amount_in_money
		form.is_everyday.data = month_type_expense.is_everyday
	return render_template('month_types/create_new_month_type.html', title='Edit Month Type', legend='Edit Month Type', form=form,
						   month_plan_id=month_plan.id)


# todo add edit month_type
