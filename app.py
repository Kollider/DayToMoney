from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '2d00df46ce74700f039ebf42idjfhijdjjc861b955121e75a765d1262b0db534994e51c76'

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
