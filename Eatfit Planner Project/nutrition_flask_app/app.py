from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from nutrition_flask_app.api_info import app_password
from flask_login import LoginManager

app = Flask(__name__)
DB_NAME = "nutrition_tb.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SECRET_KEY'] = app_password
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_signin'
from nutrition_flask_app import models
from nutrition_flask_app import views
