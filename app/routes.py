from calendar import monthrange
from datetime import datetime, date

from flask import render_template, request, flash, url_for, redirect
from flask_login import current_user, login_user, logout_user, login_required

from . import app, db, bcrypt
from .forms import SpendingForm, MonthPlanForm, MonthTypeForm, RegistrationForm, LoginForm
from .models import Spendings, Month_plans, Types_of_month_spend, Users

from .helper.daily_plan_table import delta_flow_test
from .helper.month_plan_table import plan_to_dict, daily_overall_dict
from .helper.name_months import months_names
from .helper.spend_validate import validate_spendings


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
	if current_user.status != True:
		flash('Please login to use Day to Money', 'success')
		return redirect(url_for('about'))
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
		return redirect(url_for('show_all_months'))

	a = delta_flow_test(start_checkpoint, next_checkpoint, bla, month_plan_delta.money_for_day)
	dynamic_mid = a[f'{today_date.strftime("%d.%m")}']['dynamic_mid']
	day_sum = a[f'{today_date.strftime("%d.%m")}']['day_result']
	mid_sum_delta = round(dynamic_mid+day_sum,2)

	return render_template('home.html', day_spending=day_spending, dynamic_mid=dynamic_mid, day_sum=day_sum,
						   today_date=today_date,mid_sum_delta=mid_sum_delta)


@app.route('/about')
def about():
	return render_template('about.html')


@app.route("/register", methods=['GET', 'POST'])  # todo add login redirect to the end of html
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(
			form.password.data).decode('utf-8')
		user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You are now able to log in', 'success')
		return redirect(url_for('about'))
	return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			user.status = True
			db.session.add(user)
			db.session.commit()
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)


@app.route("/logout")
@login_required
def logout():
	user = current_user
	user.status = False
	db.session.add(user)
	db.session.commit()
	logout_user()
	return redirect(url_for('home'))


@app.route('/spending/all', methods=['GET', 'POST'])
@login_required
def spendings():
	page = request.args.get('page', 1, type=int)
	day_spending = Spendings.query.filter_by(user_id=current_user.id).order_by(Spendings.id.desc()).paginate(page=page,
																											 per_page=10)

	return render_template('spendings.html', day_spending=day_spending)


@app.route('/spending/day')
@login_required
def spendings_day():
	a = request.args.get('start_day')  # todo rename variable
	b = request.args.get('day')  # todo rename variable
	c = datetime.strptime(f'{b}.{a[:4]}', '%d.%m.%Y').date()  # todo rename variable

	day_spending = Spendings.query.filter_by(user_id=current_user.id).filter(Spendings.day == c).order_by(
		Spendings.id.desc()).all()
	return render_template('spendings_day.html', day_spending=day_spending)


@app.route('/spending/new', methods=['GET', 'POST'])
@login_required
def new_spending():
	form = SpendingForm()
	if form.validate_on_submit():
		spending = Spendings(day=form.day.data,
							 name_of_item=form.name_of_item.data,
							 quantity=form.quantity.data,
							 quantity_type=form.quantity_type.data,
							 spending_amount=form.spending_amount.data,
							 user_id=current_user.id)
		validate_spendings(spending)
		db.session.add(spending)
		db.session.commit()
		flash('Your spending has been created', 'success')
		return redirect(url_for('home'))
	return render_template('create_new_spending.html', title='New Purchase', form=form, legend='New Purchase')


@app.route('/spending/<int:spending_id>')
@login_required
def spending(spending_id):
	if current_user.status != True:
		return redirect(url_for('home'))
	spending = Spendings.query.get_or_404(spending_id)
	return render_template('spending.html', title=spending.name_of_item, purchase=spending)


@app.route('/spending/<int:spending_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_spending(spending_id):
	if current_user.status != True:
		return redirect(url_for('home'))
	spending = Spendings.query.get_or_404(spending_id)
	db.session.delete(spending)
	db.session.commit()
	flash('Purchase has been deleted!', 'success')
	return redirect(url_for('home'))


@app.route('/spending/<int:spending_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_spending(spending_id):
	if current_user.status != True:
		return redirect(url_for('home'))
	spending = Spendings.query.get_or_404(spending_id)
	form = SpendingForm()
	if form.validate_on_submit():
		spending.day = form.day.data
		spending.name_of_item = form.name_of_item.data
		spending.quantity = form.quantity.data
		spending.quantity_type = form.quantity_type.data
		spending.spending_amount = form.spending_amount.data

		validate_spendings(spending)

		db.session.commit()
		flash('Purchase has been updated!', 'success')
		return redirect(url_for('spending', spending_id=spending.id))
	elif request.method == 'GET':
		form.day.data = spending.day
		form.name_of_item.data = spending.name_of_item
		form.quantity.data = spending.quantity
		form.quantity_type.data = spending.quantity_type
		form.spending_amount.data = spending.spending_amount
	return render_template('create_new_spending.html', title='Edit Purchase', legend='Edit Purchase', form=form)


@app.route('/planning/monthly/months', methods=['GET', 'POST'])
@login_required
def show_all_months():
	page = request.args.get('page', 1, type=int)
	month_plans = Month_plans.query.filter_by(user_id=current_user.id).order_by(Month_plans.month.desc()).paginate(
		page=page, per_page=5)
	return render_template('monthplanning.html', month_plans=month_plans, myfunction=months_names)


@app.route('/planning/monthly/new', methods=['GET', 'POST'])
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
		return redirect(url_for('show_all_months'))
	return render_template('create_new_month_plan.html', title='New Month Plan', form=form, legend='New Month Plan')


@app.route('/planning/monthly/<int:month_plan_id>',
		   methods=['GET', 'POST'])  # todo make adaptive to mobile screen|maybe media could help
@login_required
def month_plan_table_test(month_plan_id):
	month_plan = Month_plans.query.get_or_404(month_plan_id)
	days = monthrange(month_plan.month.year, month_plan.month.month)[1]

	return render_template('month_plan.html', title=str(month_plan.month.month) + '.' + str(month_plan.month.year),
						   month_plan=month_plan, legend='TEST LEGEND FOR MONTH PLAN',
						   planDictionary=plan_to_dict(month_plan), days=days,
						   monthOverall=daily_overall_dict(plan_to_dict(month_plan), month_plan.income))


@app.route('/planning/monthly/<int:month_plan_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_month_plan(month_plan_id):
	if not current_user.status:
		return redirect(url_for('about'))
	month_plan = Month_plans.query.get_or_404(month_plan_id)
	db.session.delete(month_plan)
	db.session.commit()
	flash('Month plan deleted successfully', 'success')
	return redirect(url_for('show_all_months'))


@app.route('/planning/monthly/<int:month_plan_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_month_plan(month_plan_id):
	if not current_user.status:
		return redirect(url_for('about'))
	month_plan = Month_plans.query.get_or_404(month_plan_id)
	form = MonthPlanForm()
	if form.validate_on_submit():
		month_plan.month = form.month.data
		month_plan.income = form.income.data
		db.session.commit()
		flash('Month plan has been edited successfully', 'success')
		return redirect(url_for('month_plan_table_test', month_plan_id=month_plan.id))
	elif request.method == 'GET':
		form.month.data = month_plan.month
		form.income.data = month_plan.income
	return render_template('create_new_month_plan.html', title='Edit Month Plan', legend='Edit Month Plan', form=form)


@app.route('/planning/monthly/types/all', methods=['GET', 'POST'])
@login_required
def show_all_types():
	page = request.args.get('page', 1, type=int)
	# plans = [plan for plan in Users.query.filter_by(id=current_user.id).first().plans]
	month_types = Types_of_month_spend.query.filter(Types_of_month_spend.month_plan.in_([plan_id.id for plan_id in
																						 [plan for plan in
																						  Users.query.filter_by(
																							  id=current_user.id).first().plans]])).order_by(
		Types_of_month_spend.id.desc()).paginate(page=page, per_page=5)
	return render_template('month_types_all.html', month_types=month_types)


@app.route('/planning/monthly/<int:month_plan_id>/types/new', methods=['GET', 'POST'])
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
		return redirect(url_for('month_plan_table_test', month_plan_id=month_plan_id))
	return render_template('create_new_month_type.html', title='New Month Type', form=form, legend='New Month Type')


@app.route('/planning/monthly/<int:month_plan_id>/types/<int:month_type_id>')
@login_required
def month_type_single(month_type_id, month_plan_id):
	if not current_user.status:
		return redirect(url_for('home'))
	month_type_expense = Types_of_month_spend.query.get_or_404(month_type_id)
	bla = month_plan_id
	return render_template('month_type_single.html', title=month_type_expense.name_of_type,
						   month_type=month_type_expense, month_plan_id=bla)


@app.route('/planning/monthly/types/<int:month_type_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_month_type(month_type_id):
	if not current_user.status:
		return redirect(url_for('home'))
	month_type_expense = Types_of_month_spend.query.get_or_404(month_type_id)
	db.session.delete(month_type_expense)
	db.session.commit()
	flash('Type has been deleted.', 'success')
	return redirect(url_for('home'))


@app.route('/planning/monthly/<int:month_plan_id>/types/<int:month_type_id>/delete', methods=['GET', 'POST'])
@login_required
def edit_month_type(month_plan_id, month_type_id):
	if not current_user.status:
		return redirect(url_for('about'))
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
		return redirect(url_for('month_type_single', month_type_id=month_type_expense.id, month_plan_id=month_plan.id))
	elif request.method == 'GET':
		form.name_of_type.data = month_type_expense.name_of_type
		form.amount_choice.data = 'money'
		form.amount.data = month_type_expense.amount_in_money
		form.is_everyday.data = month_type_expense.is_everyday
	return render_template('create_new_month_type.html', title='Edit Month Type', legend='Edit Month Type', form=form,
						   month_plan_id=month_plan.id)


# todo add edit month_type

@app.route('/planning/daily/delta_flow',
		   methods=['GET', 'POST'])  # todo add description with article above/under actual delta
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


@app.route('/planning/daily/delta_flow/test',
		   methods=['GET', 'POST'])  # todo add description with article above/under actual delta
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
