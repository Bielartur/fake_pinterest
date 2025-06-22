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
      return redirect(url_for('perfil', id_usuario=usuario.id))
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
    return redirect(url_for('perfil', id_usuario=usuario.id))
  return render_template('criarconta.html', form=form_criarconta)

@app.route('/perfil/<id_usuario>',)
@login_required
def perfil(id_usuario):
  if not (id_usuario == current_user.id):
    # O usuário está vendo o seu própio perfil
    return render_template('perfil.html', usuario=current_user.email)
  else:
    usuario = Usuario.query.get_or_404(int(id_usuario))
    return render_template('perfil.html', usuario=usuario.email)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
  logout_user()
  return redirect(url_for('homepage'))