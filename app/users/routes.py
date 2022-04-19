from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user, login_user, login_required, logout_user

from app import bcrypt, db
from app.models import Users
from app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from app.users.utils import send_reset_email

users = Blueprint('users',__name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(
			form.password.data).decode('utf-8')
		user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You are now able to log in', 'success')
		return redirect(url_for('users.login'))
	return render_template('users/register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('users/login.html', title='Login', form=form)


@users.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for('main.home'))



@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	if not current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = UpdateAccountForm()
	if form.validate_on_submit():
		current_user.email = form.email.data
		current_user.username = form.username.data
		db.session.commit()
		flash('Account info has been updated!', 'success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.email.data = current_user.email
		form.username.data = current_user.username
	return render_template('users/account.html', title='Account', form=form)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
	form = RequestResetForm()
	if current_user.is_authenticated:
		form.email.data = current_user.email
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('Please, check your mailbox and spam folder. Email with instructions has been sent.', 'info')
		return redirect(url_for('users.login'))
	return render_template('users/reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
	# if current_user.is_authenticated:
	# 	return redirect(url_for('main.home'))
	user = Users.verify_reset_token(token)
	if user is None:
		flash('Invalid or expired token', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(
			form.password.data).decode('utf-8')
		user.password=hashed_password
		db.session.commit()
		flash('Your password has been changed!', 'success')
		return redirect(url_for('users.login'))
	return render_template('users/reset_token.html', title='Reset Password', form=form)

