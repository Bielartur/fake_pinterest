from flask_login import UserMixin
from sqlalchemy.testing.pickleable import User

from fakepinterest import database, login_manager
from datetime import datetime

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80), nullable=False)
    email = database.Column(database.String(255), nullable=False, unique=True)
    senha = database.Column(database.String(255), nullable=False)
    fotos = database.relationship('Foto', backref='usuario', lazy=True)

class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String(255), default='default.png')
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.now)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)