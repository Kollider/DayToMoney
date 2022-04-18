from datetime import datetime

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.helper.spend_validate import validate_spendings
from app.models import Spendings
from app.spendings.forms import SpendingForm

spendings = Blueprint('spendings',__name__)


@spendings.route('/spending/all', methods=['GET', 'POST'])
@login_required
def _spendings():
	page = request.args.get('page', 1, type=int)
	day_spending = Spendings.query.filter_by(user_id=current_user.id).order_by(Spendings.id.desc()).paginate(page=page,
																											 per_page=10)

	return render_template('spendings/spendings.html', day_spending=day_spending)


@spendings.route('/spending/day')
@login_required
def spendings_day():
	a = request.args.get('start_day')  # todo rename variable
	b = request.args.get('day')  # todo rename variable
	c = datetime.strptime(f'{b}.{a[:4]}', '%d.%m.%Y').date()  # todo rename variable

	day_spending = Spendings.query.filter_by(user_id=current_user.id).filter(Spendings.day == c).order_by(
		Spendings.id.desc()).all()
	return render_template('spendings/spendings_day.html', day_spending=day_spending)


@spendings.route('/spending/new', methods=['GET', 'POST'])
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
		return redirect(url_for('main.home'))
	return render_template('spendings/create_new_spending.html', title='New Purchase', form=form, legend='New Purchase')


@spendings.route('/spending/<int:spending_id>')
@login_required
def spending(spending_id):
	if not current_user.is_authenticated:
		return redirect(url_for('main.home'))
	spending = Spendings.query.get_or_404(spending_id)
	return render_template('spendings/spending.html', title=spending.name_of_item, purchase=spending)


@spendings.route('/spending/<int:spending_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_spending(spending_id):
	if not current_user.is_authenticated:
		return redirect(url_for('main.home'))
	spending = Spendings.query.get_or_404(spending_id)
	db.session.delete(spending)
	db.session.commit()
	flash('Purchase has been deleted!', 'success')
	return redirect(url_for('main.home'))


@spendings.route('/spending/<int:spending_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_spending(spending_id):
	if not current_user.is_authenticated:
		return redirect(url_for('main.home'))
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
		return redirect(url_for('spendings.spending', spending_id=spending.id))
	elif request.method == 'GET':
		form.day.data = spending.day
		form.name_of_item.data = spending.name_of_item
		form.quantity.data = spending.quantity
		form.quantity_type.data = spending.quantity_type
		form.spending_amount.data = spending.spending_amount
	return render_template('spendings/create_new_spending.html', title='Edit Purchase', legend='Edit Purchase', form=form)
