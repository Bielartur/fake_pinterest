from flask import render_template, url_for, redirect
from flask_login import login_required, login_user, logout_user, current_user

from fakepinterest import app, database, bcrypt
from fakepinterest.forms import FormLogin, FormCriarConta
from fakepinterest.models import Usuario


@app.route('/', methods=['GET', 'POST'])
def homepage():
  formlogin = FormLogin()
  if formlogin.validate_on_submit():
    usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
    if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
      login_user(usuario)
      return redirect(url_for('perfil', usuario=usuario.username))
  return render_template('homepage.html', form=formlogin)

@app.route('/criarconta', methods=['GET', 'POST'])
def criarconta():
  form_criarconta = FormCriarConta()
  if form_criarconta.validate_on_submit():
    senha = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
    usuario = Usuario(
      username=form_criarconta.username.data,
      email=form_criarconta.email.data,
      senha=senha,
    )
    database.session.add(usuario)
    database.session.commit()
    login_user(usuario, remember=True)
    return redirect(url_for('perfil', usuario=usuario.username))
  return render_template('criarconta.html', form=form_criarconta)

@app.route('/perfil/<usuario>',)
@login_required
def perfil(usuario):
  return render_template('perfil.html', usuario=usuario)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
  logout_user()
  return redirect(url_for('homepage'))