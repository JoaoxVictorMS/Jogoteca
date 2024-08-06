from jogoteca import app
from flask import render_template, request, redirect, session, flash, url_for
from models import Usuarios
from helpers import FormularioUsuario
from flask_bcrypt import check_password_hash
# Rota para login
@app.route('/login')
def login():
    proxima = request.args.get('proxima')

    #Instância da classe FormularioUsuario
    form = FormularioUsuario(request.form)

    # Caso a verificação da variável "proxima" não for igual a none, ela recebera o index, indicando que o usuário logou com êxito
    if proxima == None:
        return render_template('login.html', proxima=url_for('index'), form=form)
    # Enviando as informações da proxima página para login.html
    return render_template('login.html', proxima=proxima, form=form)

# Tora que de fato autentica e loga o usuário
@app.route('/autenticar', methods=['POST',])
def autenticar():
    #Instância da classe FormularioUsuario
    form = FormularioUsuario(request.form)

    # Caso exista algum nickname na tabela de Usuario que bata com o o nickname digitado pelo usuário, o resultado será salvo na variável (True or False)
    # .first() retorna o primeiro resultado
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()

    # Descriptografa e senha e a retorna
    senha = check_password_hash(usuario.senha, form.senha.data)

    # Verifica se o usuario existe na lista de usuários através do nickname
    if usuario and senha:
        # Verfica se a senha do usuário está correta
        # Salva o nickname do usuário dentro de session
        session['usuario_logado'] = usuario.nickname
        # Emite uma mensagem rápida e única
        flash(usuario.nickname + ' logado com sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)
    else:
        flash('Usuário não logado')
        return redirect(url_for('login'))

# Rota de logout
@app.route('/logout')
def logout():
    # Limpa a session e as credenciais do usuário atualmente logado
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso')
    return redirect(url_for('index'))