from calendar import monthrange
from datetime import datetime

from flask import render_template, request, flash, url_for, redirect

from new_app.forms import SpendingForm, MonthPlanForm, MonthTypeForm
from new_app.helper.month_plan_table import plan_to_dict, daily_overall_dict
from new_app.helper.name_months import months_names
from new_app.main import website, db
from new_app.models import Spendings, Month_plans, Types_of_month_spend


@website.route("/")
@website.route("/home", methods=['GET', 'POST'])
def home():
	page = request.args.get('page', 1, type=int)
	start_checkpoint = datetime.strptime('01.09.2021', '%d.%m.%Y').date()
	next_checkpoint = datetime.strptime('30.09.2021', '%d.%m.%Y').date()
	delta = next_checkpoint - start_checkpoint
	day_spendings = Spendings.query.filter(Spendings.day >= start_checkpoint, Spendings.day <= next_checkpoint)
	return render_template('home.html', day_spendings=day_spendings)


@website.route('/spendings', methods=['GET', 'POST'])
def spendings():
	page = request.args.get('page', 1, type=int)
	day_spending = Spendings.query.order_by(Spendings.id.desc()).paginate(page=page, per_page=5)
	return render_template('spendings.html', day_spending=day_spending)

@website.route('/spending/new',methods=['GET', 'POST'])
def new_spending():
	form=SpendingForm()
	if form.validate_on_submit():
		spending=Spendings(day=form.day.data,name_of_item=form.name_of_item.data,quantity=form.quantity.data,quantity_type=form.quantity_type.data,spending_amount=form.spending_amount.data,user_id=1)
		db.session.add(spending)
		db.session.commit()
		flash('Your spending has been created','success')
		return redirect(url_for('home'))
	return render_template('create_new_spending.html',title='New Spending', form=form, legend='New Spending')

@website.route('/planning/monthly/months',methods=['GET', 'POST'])
def show_all_months():
	page = request.args.get('page', 1, type=int)
	month_plans=Month_plans.query.order_by(Month_plans.id.desc()).paginate(page=page, per_page=5)
	return render_template('monthplanning.html', month_plans=month_plans,myfunction=months_names)

@website.route('/planning/monthly/new',methods=['GET', 'POST'])
def month_plan_new():
	form=MonthPlanForm()
	if form.validate_on_submit():
		monthplan=Month_plans(month=form.month.data,income=form.income.data,money_for_month=0,money_for_day= 0) #todo change 0 to actual value calculated by plan| maybe add more if-coditions to calculate values properly?
		db.session.add(monthplan)
		db.session.commit()
		flash('Your month plan has been created', 'success')
		return redirect(url_for('home'))
	return render_template('create_new_month_plan.html', title='New Month Plan', form=form, legend='New Month Plan')

@website.route('/planning/monthly/types/all',methods=['GET', 'POST'])
def show_all_types():
	page = request.args.get('page', 1, type=int)
	month_types=Types_of_month_spend.query.order_by(Types_of_month_spend.id.desc()).paginate(page=page, per_page=5)
	return render_template('month_types_all.html', month_types=month_types)

@website.route('/planning/monthly/types/new',methods=['GET', 'POST'])
def month_type_new():
	form=MonthTypeForm()
	if form.validate_on_submit():
		monthtype=Types_of_month_spend(name_of_type=form.name_of_type.data,amount_in_percent=form.amount_in_percent.data,amount_in_money=form.amount_in_money.data,is_default=form.is_default.data,is_everyday=form.is_everyday.data,month_plan=form.month_plan.data) #todo change 0 to actual value calculated by plan| maybe add more if-coditions to calculate values properly?
		db.session.add(monthtype)
		db.session.commit()
		flash('Your month plan has been created', 'success')
		return redirect(url_for('home'))
	return render_template('create_new_month_type.html', title='New Month Type', form=form, legend='New Month Type')


@website.route('/planning/monthly/<int:month_plan_id>',methods=['GET', 'POST'])
def month_plan_table_test(month_plan_id):
	month_plan = Month_plans.query.get_or_404(month_plan_id)
	days=monthrange(month_plan.month.year, month_plan.month.month)[1]

	return render_template('month_plan.html', title=str(month_plan.month.month)+'.'+str(month_plan.month.year), month_plan=month_plan, legend='TEST LEGEND FOR MONTH PLAN', planDictionary=plan_to_dict(month_plan), days=days, monthOverall=daily_overall_dict(plan_to_dict(month_plan)))

