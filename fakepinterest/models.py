from flask_login import UserMixin
from fakepinterest import database, login_manager
from datetime import datetime

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80), nullable=False, unique=True)
    email = database.Column(database.String(255), nullable=False, unique=True)
    senha = database.Column(database.String(255), nullable=False)
    fotos = database.relationship('Foto', backref='usuario', lazy=True)
    foto_perfil = database.relationship('FotoPerfil', backref=database.backref('usuario', uselist=False), uselist=False, lazy=True, cascade='all, delete-orphan')

class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String(255), default='default.png')
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.now)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

class FotoPerfil(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String(255), default='user-default.png')
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
