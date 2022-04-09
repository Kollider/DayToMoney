from calendar import monthrange
from datetime import datetime

from flask import render_template, request, flash, url_for, redirect
from flask_login import current_user, login_user, logout_user, login_required

from new_app.forms import SpendingForm, MonthPlanForm, MonthTypeForm, RegistrationForm, LoginForm
from new_app.helper.daily_plan_table import delta_flow_test
from new_app.helper.month_plan_table import plan_to_dict, daily_overall_dict
from new_app.helper.name_months import months_names
from new_app.helper.spend_validate import validate_spendings
from new_app.main import website, db, bcrypt
from new_app.models import Spendings, Month_plans, Types_of_month_spend, Users


@website.route("/")
@website.route("/home", methods=['GET', 'POST'])
def home():
	page = request.args.get('page', 1, type=int)
	start_checkpoint = datetime.strptime('01.09.2021', '%d.%m.%Y').date()
	next_checkpoint = datetime.strptime('30.09.2021', '%d.%m.%Y').date()
	delta = next_checkpoint - start_checkpoint
	day_spendings = Spendings.query.filter(Spendings.day >= start_checkpoint, Spendings.day <= next_checkpoint)
	return render_template('home.html')


@website.route("/register", methods=['GET', 'POST'])  # todo add login redirect to the end of html
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
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)


@website.route("/login", methods=['GET', 'POST'])
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


@website.route("/logout")
@login_required
def logout():
	user = current_user
	user.status = False
	db.session.add(user)
	db.session.commit()
	logout_user()
	return redirect(url_for('home'))


@website.route('/spendings', methods=['GET', 'POST'])
def spendings():
	page = request.args.get('page', 1, type=int)
	day_spending = Spendings.query.filter_by(user_id=current_user.id).order_by(Spendings.id.desc()).paginate(page=page, per_page=5)
	return render_template('spendings.html', day_spending=day_spending)


@website.route('/spending/new', methods=['GET', 'POST'])
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
	return render_template('create_new_spending.html', title='New Spending', form=form, legend='New Spending')


@website.route('/planning/monthly/months', methods=['GET', 'POST'])
@login_required
def show_all_months():
	page = request.args.get('page', 1, type=int)
	month_plans = Month_plans.query.filter_by(user_id=current_user.id).order_by(Month_plans.id.desc()).paginate(page=page, per_page=5)
	return render_template('monthplanning.html', month_plans=month_plans, myfunction=months_names)


@website.route('/planning/monthly/new', methods=['GET', 'POST'])
@login_required
def month_plan_new():
	form = MonthPlanForm()
	if form.validate_on_submit():
		monthplan = Month_plans(month=form.month.data,
								income=form.income.data,
								money_for_month=0, # todo change 0 to actual value calculated by plan| maybe add more if-coditions to calculate values properly?
								money_for_day=form.income.data,
								user_id=current_user.id)
		db.session.add(monthplan)
		db.session.commit()
		flash('Your month plan has been created', 'success')
		return redirect(url_for('home'))
	return render_template('create_new_month_plan.html', title='New Month Plan', form=form, legend='New Month Plan')


@website.route('/planning/monthly/types/all', methods=['GET', 'POST'])
@login_required
def show_all_types():
	page = request.args.get('page', 1, type=int)
	#plans = [plan for plan in Users.query.filter_by(id=current_user.id).first().plans]
	month_types = Types_of_month_spend.query.filter(Types_of_month_spend.month_plan.in_([plan_id.id for plan_id in [plan for plan in Users.query.filter_by(id=current_user.id).first().plans]])).order_by(Types_of_month_spend.id.desc()).paginate(page=page, per_page=5)
	return render_template('month_types_all.html', month_types=month_types)


@website.route('/planning/monthly/<int:month_plan_id>/types/new', methods=['GET', 'POST'])
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


@website.route('/planning/monthly/<int:month_plan_id>',
			   methods=['GET', 'POST'])  # todo make adaptive to mobile screen|maybe media could help
@login_required
def month_plan_table_test(month_plan_id):
	month_plan = Month_plans.query.get_or_404(month_plan_id)
	days = monthrange(month_plan.month.year, month_plan.month.month)[1]

	return render_template('month_plan.html', title=str(month_plan.month.month) + '.' + str(month_plan.month.year),
						   month_plan=month_plan, legend='TEST LEGEND FOR MONTH PLAN',
						   planDictionary=plan_to_dict(month_plan), days=days,
						   monthOverall=daily_overall_dict(plan_to_dict(month_plan), month_plan.income))


@website.route('/planning/daily/delta_flow',
			   methods=['GET', 'POST'])  # todo add description with article above/under actual delta
@login_required
def delta_flow():
	start_checkpoint = datetime.strptime('01.09.2021', '%d.%m.%Y').date()  # todo create form to choose date
	next_checkpoint = datetime.strptime('30.09.2021', '%d.%m.%Y').date()  # todo maybe add formFIELDS to choose date with button to redirect to itself on top of the delta

	bla = Spendings.query.filter_by(user_id=current_user.id).filter(Spendings.day >= start_checkpoint,
																	Spendings.day <= next_checkpoint)  # todo change to normal name

	month_plan_id = 1
	month_plan_delta = Month_plans.query.get_or_404(
		month_plan_id)  # todo think about an actual way to obtain month_id| should it be passed or queued in some way?
	b = month_plan_delta.money_for_day

	a = delta_flow_test(start_checkpoint, next_checkpoint, bla, month_plan_delta.money_for_day)

	return render_template('delta_flow.html', delta_flow_results=a, start_checkpoint=start_checkpoint.strftime("%d.%m.%y"),
						   next_checkpoint=next_checkpoint.strftime("%d.%m.%y"),
						   prev_checkpoint=b)  # todo check naming #todo format dates to human-friendly


@website.route('/planning/daily/delta_flow/test',
			   methods=['GET', 'POST'])  # todo add description with article above/under actual delta
@login_required
def delta_flow_month():
	month_plan_id = request.args.get('month_plan_id')
	month_plan_delta = Month_plans.query.get_or_404(month_plan_id)
	start_checkpoint = datetime.strptime('01.'+f'{month_plan_delta.month.month}.{month_plan_delta.month.year}', '%d.%m.%Y').date()  # todo create form to choose date
	next_checkpoint = datetime.strptime(f'{monthrange(month_plan_delta.month.year, month_plan_delta.month.month)[1]}.{month_plan_delta.month.month}.{month_plan_delta.month.year}','%d.%m.%Y').date()  # todo maybe add formFIELDS to choose date with button to redirect to itself on top of the delta
	bla = Spendings.query.filter_by(user_id=current_user.id).filter(Spendings.day >= start_checkpoint,
																	Spendings.day <= next_checkpoint)  # todo change to normal name

	b = month_plan_delta.money_for_day

	a = delta_flow_test(start_checkpoint, next_checkpoint, bla, month_plan_delta.money_for_day)

	return render_template('delta_flow.html', delta_flow_results=a, start_checkpoint=start_checkpoint,
						   next_checkpoint=next_checkpoint,
						   prev_checkpoint=b)# todo check naming #todo format dates to human-friendly
