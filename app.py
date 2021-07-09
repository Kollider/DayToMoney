from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '2d00df46ce74700f039ebf42idjfhijdjjc861b955121e75a765d1262b0db534994e51c76'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    day_spendings = db.relationship('Day_spending', backref='User_that_spent',lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}' '{self.image_file}')"

class Day_spending(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    date_spent = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    quantity = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.type}','{self.date_spent}' '{self.quantity}')"


day_spendings = [
    {
        'date': '01.07.2021',
        'type': 'apple',
        'quantity': '548',
        'quantity_type': 'g'
    },
    {
        'date': '01.07.2021',
        'type': 'metro',
        'quantity': '2',
        'quantity_type': 'item'
    }
]




@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', day_spendings=day_spendings)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created successfully for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@test.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed! Check your username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
