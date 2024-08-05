# Biblioteca flask e a classe Flask
# render_template carrega algum template, em html, que desejar, tal qual informacões que são dadas pelos parâmetros
# request é um helper que ajuda a capturar dados e informações
# Session é um recurso do Flask que permite um armazenamento temporário de dados que persiste as informações coletadas por mais de um ciclo de request.
# flash é uma função que emite mensagens rápidas e únicas no navegador
# BOA PRÁTICA - url_for torna as urls mais dunâmicas e fáceis de alterar, não precisando ficar procurando no código a url que deseja alterar
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Jogos
from helpers import recupera_imagem, deleta_arquivo, FormularioJogo
import time
# Rota para a página de início
# Adicionando o decorador route() para dizer ao FLask qual url deve ser acionada pela função
@app.route('/')
# A função retorna o template ou mensagem no navegador
def index():
    # Query que busca os jogos e os oredena através do id
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Jogos', jogos=lista)

# Rota para a página de formulário para novos jogos
@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        # ?proxima=novo é uma querySTring indicando para a próxima página que será acessada
        return redirect(url_for('login', proxima=url_for('novo')))
    # Instância da classe FormularioJogo
    form = FormularioJogo()
    return render_template('novo.html', titulo='Novo Jogo', form=form)

# Rota para edição de algum jogo específico
# Colocando o <int:id> e o id como parâmetro da função editar, a aplicação saberá qual jogo especificamente queremos editar, puxando suas informações.
# Em lista.html, foi passado esse id na url do editar 
@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        # ?proxima=novo é uma querySTring indicando para a próxima página que será acessada
        return redirect(url_for('login', proxima=url_for('editar')))
    
    # Fazendo a busca do jogo específico no banco de dados através da query abaixo
    jogo = Jogos.query.filter_by(id=id).first()
    # Instância da classe FormularioJogo
    form = FormularioJogo()
    # o .data acessa os valores de um determinado input, no caso o nome
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console
    capa_jogo = recupera_imagem(id)
    # retorna a variável jogo contendo a query
    # Os parâmetros do render_template passam informações para o html 
    return render_template('editar.html', titulo='Editando Jogo',id=id, capa_jogo=capa_jogo, form=form)

# Roda que de fato atualiza as informações editadas
@app.route('/atualizar', methods=['POST',])
def atualizar():
     # Instância da classe FormularioJogo mas passando as informações do formulário ja adquiridas
    form = FormularioJogo(request.form)

    if form.validate_on_submit():
        # Pega as informações do jogo através do id do mesmo passado pela requisição (informado no formulário) no site feito pelo usuário
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        # Atualiza os campos do jogo específico
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data

        # Alterando(adicionando o jogo) o novo jogo na tabela Jogos através da instância do banco de dados do SQLAlchemy
        db.session.add(jogo)
        # Commit das alterações; Salva a transação de dados
        db.session.commit()

        #['arquivo'] é a tah bame no front end
        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        # time() será responsável por deixar o nome de cada imagem único pois devolverá o segundos exatos que cada imagem foi inserida
        timestamp = time.time()
        # Deleta uma imagem
        deleta_arquivo(jogo.id)
        # Passando o time na formatação do nome da imagem
        arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

# Rota para deleção de algum jogo
@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    
    Jogos.query.filter_by(id=id).delete()
    # Commit das alterações; Salva a transação de dados
    db.session.commit()
    flash('Jogo deletado com sucesso!')
    return redirect(url_for('index'))

# Rota que de fato cadastra e cria o jogo requisitado para cadastro. Rota de processamento. Página intermerdiária
# E necessário também fornecer para a rota qual o método será utilizado, pois por padrão é o GET
@app.route('/criar', methods=['POST',])
def criar():
    #Instância da classe FormularioJogo
    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    # request.form captura as informações das tags name dos insputs em novo.html
    nome = form.nome.data
    categoria = form.nome.categoria
    console = form.nome.console

    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash('Jogo já existe!')
        return redirect(url_for('index'))

    # Instância do novo jogo adicionado pelo usuário
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    # Inserindo o novo jogo na tabela Jogos através da instância do banco de dados do SQLAlchemy
    db.session.add(novo_jogo)
    # Commit do novo jogo; salva a transação de dados
    db.session.commit()

    #['arquivo'] é a tah bame no front end
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    # time() será responsável por deixar o nome de cada imagem único pois devolverá o segundos exatos que cada imagem foi inserida
    timestamp = time.time()
    # Passando o time na formatação do nome da imagem
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg')

    # Renderiza a lista de jogos
    # url_for recebe a FUNÇÃO que instancia a página html
    return redirect(url_for('index'))



# Essa rota serve exclusivamente para enviar a imagem placeholder para o arquivo novo.html, mais especificamente na tag figure
@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    #send_from_directory returna algo de algum diretório dado
    return send_from_directory('uploads', nome_arquivo)


