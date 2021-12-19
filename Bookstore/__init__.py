from flask_admin import Admin
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = '@#$%^876$%^&*OIUYTRTYUIJHG^&*((*&^$%^&*'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/bookstore?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)

loginn = LoginManager(app=app)

cloudinary.config(cloud_name='dxxwcby8l',
                  api_key='448651448423589',
                  api_secret='ftGud0r1TTqp0CGp5tjwNmkAm-A')
