from flask import (
    render_template, request, redirect,
    url_for, flash, current_app
)
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.utils import secure_filename
import os

from fakepinterest import app, database, bcrypt
from fakepinterest.models import Usuario, Foto, FotoPerfil
from fakepinterest.forms import FormFoto, FormLogin, FormCriarConta, FormEditarPerfil

def salvar_foto_perfil(file_storage, user_id):
    filename = secure_filename(file_storage.filename)
    upload_folder = current_app.config['UPLOAD_FOLDER_PERFIL']
    os.makedirs(os.path.join(current_app.root_path, upload_folder), exist_ok=True)
    path = os.path.join(current_app.root_path, upload_folder, filename)
    file_storage.save(path)
    return filename

@app.route('/', methods=['GET', 'POST'])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.login.data).first()
        if not usuario:
            usuario = Usuario.query.filter_by(username=formlogin.login.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for('feed'))
    return render_template('homepage.html', form=formlogin)

@app.route('/criarconta', methods=['GET', 'POST'])
def criarconta():
    form = FormCriarConta()
    if form.validate_on_submit():
        # 1) Cria o usuário
        hashed = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        usuario = Usuario(
            username=form.username.data,
            email=form.email.data,
            senha=hashed
        )

        # 2) Prepara objeto de foto (padrão) em memória
        if form.foto.data:
            filename = salvar_foto_perfil(form.foto.data, None)
            usuario.foto_perfil = FotoPerfil(imagem=filename)
        else:
            # caso sem upload ou inválido, vai usar imagem padrão definida no model
            usuario.foto_perfil = FotoPerfil()

        # 3) Persiste tudo de uma vez
        database.session.add(usuario)
        database.session.commit()

        # 4) Login e redirecionamento
        login_user(usuario, remember=True)
        flash('Conta criada com sucesso!', 'success')
        return redirect(url_for('feed'))

    # GET ou erro de validação
    return render_template('criarconta.html', form=form)

@app.route('/perfil/<int:id_usuario>', methods=['GET', 'POST'])
@login_required
def perfil(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)

    # 1) Se for o perfil de outra pessoa, só exibe
    if usuario.id != current_user.id:
        return render_template(
            'perfil.html',
            usuario=usuario,
            form_foto=None,
        )

    # 2) É o próprio usuário: instancia os dois formulários
    form_foto   = FormFoto()

    # 3) DELETE de imagem de post
    if request.method == 'POST' and request.form.get('deletar-imagem'):
        foto_id = int(request.form['deletar-imagem'])
        foto = Foto.query.get_or_404(foto_id)
        if foto.id_usuario == current_user.id:
            database.session.delete(foto)
            database.session.commit()
            flash('Foto deletada com sucesso.', 'success')
        return redirect(url_for('perfil', id_usuario=usuario.id))

    # 4) UPLOAD de nova foto de POST
    if 'botao_post' in request.form and form_foto.validate():
        arquivo    = form_foto.foto.data
        nome_seg   = secure_filename(arquivo.filename)
        pasta_post = current_app.config['UPLOAD_FOLDER_POSTS']
        caminho    = os.path.join(current_app.root_path, pasta_post, nome_seg)
        arquivo.save(caminho)

        nova = Foto(imagem=nome_seg, id_usuario=current_user.id)
        database.session.add(nova)
        database.session.commit()
        flash('Postagem adicionada com sucesso!', 'success')
        return redirect(url_for('perfil', id_usuario=usuario.id))

    return render_template(
        'perfil.html',
        usuario=usuario,
        form_foto=form_foto,
    )

@app.route('/editar_perfil/<id_usuario>', methods=['GET', 'POST'])
@login_required
def editar_perfil(id_usuario):

    if int(id_usuario) != current_user.id:
        return redirect(url_for('perfil', id_usuario=current_user.id))
    usuario = Usuario.query.get(current_user.id)

    form_perfil = FormEditarPerfil()

    if form_perfil.validate_on_submit():
        # Atualiza se já existir, senão cria
        usuario.username = form_perfil.username.data if form_perfil.username.data else current_user.username
        usuario.email = form_perfil.email.data if form_perfil.email.data else current_user.email

        if form_perfil.foto.data:
            nome_seg = salvar_foto_perfil(form_perfil.foto.data, current_user.id)

            if usuario.foto_perfil:
                usuario.foto_perfil.imagem = nome_seg
            else:
                fp = FotoPerfil(imagem=nome_seg, id_usuario=current_user.id)
                database.session.add(fp)

        database.session.commit()
        flash('Foto de perfil atualizada com sucesso!', 'success')
        return redirect(url_for('perfil', id_usuario=usuario.id))

    return render_template('editarperfil.html', usuario=usuario, form=form_perfil)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/feed')
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template('feed.html', fotos=fotos)
