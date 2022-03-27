from datetime import datetime

from flask import render_template, request, flash, url_for, redirect

from new_app.forms import SpendingForm
from new_app.main import website, db
from new_app.models import Spendings


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