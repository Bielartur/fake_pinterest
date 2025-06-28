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
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        # Cria o usuário
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
        usuario = Usuario(
            username=form_criarconta.username.data,
            email=form_criarconta.email.data,
            senha=senha,
        )
        database.session.add(usuario)
        database.session.commit()

        # Cria define uma foto padrão ao usuário
        usuario = Usuario.query.filter_by(username=form_criarconta.username.data).first()

        if form_criarconta.foto.data:
            arquivo = form_criarconta.foto.data
            nome_seg = secure_filename(arquivo.filename)
            pasta_perfil = current_app.config['UPLOAD_FOLDER_PERFIL']
            caminho = os.path.join(current_app.root_path, pasta_perfil, nome_seg)
            arquivo.save(caminho)

            if usuario.foto_perfil:
                usuario.foto_perfil.imagem = nome_seg
            else:
                fp = FotoPerfil(imagem=nome_seg, id_usuario=usuario.id)
                database.session.add(fp)
        else:
            fp = FotoPerfil(id_usuario=usuario.id)
            database.session.add(fp)

        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for('feed'))
    return render_template('criarconta.html', form=form_criarconta)


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
            form_perfil=None
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

    # 5) GET: renderiza ambos os formulários para edição
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

    if request.method == 'POST':
        print('> request.files:', request.files)  # deve ter chave 'foto'
        print('> request.form:', request.form)

    form_perfil = FormEditarPerfil()

    if form_perfil.validate_on_submit():
        # Atualiza se já existir, senão cria
        usuario.username = form_perfil.username.data if form_perfil.username.data else current_user.username
        usuario.email = form_perfil.email.data if form_perfil.email.data else current_user.email

        if form_perfil.foto.data:
            arquivo = form_perfil.foto.data
            nome_seg = secure_filename(arquivo.filename)
            pasta_perfil = current_app.config['UPLOAD_FOLDER_PERFIL']
            caminho = os.path.join(current_app.root_path, pasta_perfil, nome_seg)
            arquivo.save(caminho)

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
