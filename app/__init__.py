from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Config Values
UPLOAD_FOLDER = './app/static/uploads'


app = Flask(__name__)
app.config['SECRET_KEY'] = "random_key"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://amdbkzxhnsbpfj:a015b33567c1f1c00f93ddd81b3ef2dce46ff88311c6e86c73f49782b7a60c5c@ec2-52-45-14-227.compute-1.amazonaws.com:5432/d49med9sk8pn77"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

db = SQLAlchemy(app)

app.config.from_object(__name__)
from app import views
