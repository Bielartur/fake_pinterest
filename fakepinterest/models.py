from datetime import datetime

from fakepinterest import database


class Usuario(database.Model):
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