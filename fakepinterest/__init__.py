from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
app = Flask(__name__)

load_dotenv()
if int(os.getenv('DEBUG')) == 0:
    LINK_BANCO = os.getenv('DATABASE_URL')
else:
    LINK_BANCO = 'sqlite:///comunidade.db'

app.config['SQLALCHEMY_DATABASE_URI'] = LINK_BANCO
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = 'static/fotos_posts'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'homepage'

from fakepinterest import routes