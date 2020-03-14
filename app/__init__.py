from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Config Values
UPLOAD_FOLDER = './app/static/uploads'


app = Flask(__name__)
app.config['SECRET_KEY'] = "random_key"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://xuqbiiebtirbdm:75937ea6212a88bcb04060b2912557dfb4ecf73933b0805f7cd6aad44999f20d@ec2-35-172-85-250.compute-1.amazonaws.com:5432/demdudd69iu1e8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

db = SQLAlchemy(app)

app.config.from_object(__name__)
from app import views
