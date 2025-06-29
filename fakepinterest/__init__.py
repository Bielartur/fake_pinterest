from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_talisman import Talisman
from dotenv import load_dotenv
import os

app = Flask(__name__)

csp = {
    'default-src': ["'self'"],

    # libera CSS externo + inline
    'style-src': [
        "'self'",
        "'unsafe-inline'",              # → autoriza style="…" e <style> inline
        'https://fonts.googleapis.com', # Google Fonts
        'https://cdnjs.cloudflare.com'  # Font Awesome CSS
    ],

    # libera fontes externas do Google e do Cloudflare (Font Awesome)
    'font-src': [
        "'self'",
        'https://fonts.gstatic.com',    # Google Fonts
        'https://cdnjs.cloudflare.com'  # Font Awesome woff/woff2
    ],

    'img-src': [
        "'self'"
    ],

    'script-src': [
        "'self'"
    ]
}

# Aplica o Talisman com força de HTTPS e a CSP acima
Talisman(
    app,
    force_https=True,
    content_security_policy=csp
)

load_dotenv()
if int(os.getenv('DEBUG')) == 0:
    db_url = os.getenv('DATABASE_URL')
    # SQLAlchemy 2.x precisa de 'postgresql://', não 'postgres://'
    if db_url and db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    LINK_BANCO = db_url
else:
    LINK_BANCO = 'sqlite:///comunidade.db'

app.config['SQLALCHEMY_DATABASE_URI'] = LINK_BANCO
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER_POSTS'] = 'static/fotos_posts'
app.config['UPLOAD_FOLDER_PERFIL'] = 'static/fotos_perfil'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'homepage'

# === CRIAÇÃO AUTOMÁTICA DE TABELAS ===
@app.before_first_request
def criar_tabelas():
    database.create_all()

from fakepinterest import routes