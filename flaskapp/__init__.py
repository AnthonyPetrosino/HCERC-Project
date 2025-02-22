# Package application
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key76543267' # TODO Change
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # Establish relative path from app.py to db
db = SQLAlchemy(app)    # SQAlchemy instance
bcrypt = Bcrypt(app)    # Password encryption
LoginManager = LoginManager(app)    # User login functionality
LoginManager.login_view = 'login'
LoginManager.login_message_category = 'info'

from flaskapp import routes