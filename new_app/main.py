from flask import Flask
from flask_sqlalchemy import SQLAlchemy


website = Flask(__name__)
website.config['SECRET_KEY'] = '2d00df46ce74700f039ebf42idjfhijdjjc861b955121e75a765d1262b0db534994e51c76'
website.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
website.config["DEBUG"] = True

db = SQLAlchemy(website)

import routes