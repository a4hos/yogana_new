from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


#setting up a project - App name, DB, Secret key
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yogana.db'
app.config['SECRET_KEY'] = 'yu74378cfc6c726ae4041516g'

# Configurations for development mode
app.config['DEBUG'] = True

# Configurations for production mode
# Comment the line above and uncomment the line below when deploying to production
# app.config['DEBUG'] = False


#Initializing SQL Alchemy
db = SQLAlchemy(app)

#Initializing Bcrypt - password hashing
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"


#Initializing Login Manager
from yogana import routes