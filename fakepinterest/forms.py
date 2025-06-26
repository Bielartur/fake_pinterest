from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from fakepinterest.models import Usuario


class FormLogin(FlaskForm):
    login = StringField('E-mail ou nome de usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    botao_confirmacao = SubmitField('Fazer Login')

    def validate_login(self, login):
        """Aceita tanto e-mail quanto username:
           1) se tiver '@' → valida formato com Email()
           2) procura no banco por email OU username
        """
        texto = login.data.strip()
        usuario = None
        # 1) Se parece ser e-mail, valide formato RFC
        if '@' in texto:
            email_validator = Email('Email inválido')
            email_validator(self, login)
            # busca o cadastro do usuário pelo email
            usuario = Usuario.query.filter_by(email=texto).first()

        # caso ainda não tenha achado o usuário, busca pelo username
        if not usuario:
            usuario = Usuario.query.filter_by(username=texto).first()

        if not usuario:
            raise ValidationError('Usuário inexistente, crie uma conta')


class FormCriarConta(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('senha')])
    botao_confirmacao = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado, faça login para continuar')

    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError('Nome de usuário já cadastrado, faça login para continuar')


class FormFoto(FlaskForm):
    foto = FileField('Foto', validators=[DataRequired()])
    botao_confirmacao = SubmitField('Enviar')