from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt


# Código antes de implementar o banco de dados e o ORM
'''
class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


# Passando estas variáveis de forma global
jogo1 = Jogo('Minecraft', 'Sobrevivência', 'Multiplataforma')
jogo2 = Jogo('GTAV', 'Ação e Aventura', 'Multiplataforma')
jogo3 = Jogo('Rainbow Six Siege', 'FPS', 'Multiplataforma')
# Colocando os jogos numa lista e atribundo a mesma para a variável lista
lista = [jogo1, jogo2, jogo3]
# Não é uma boa prática fazer alterações diretas no html, como, por exemplo, mudar o título da página.
# Usamos o Flask para tal finalidade através de código embedado -> {{  }}.
# No caso passando a variável titulo, que se encontra no lista.html, juntamente com um valor atribuido a ela, como parâmetro do render_template

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario("Joao" , "joao_trena", "4100")
usuario2 = Usuario("Pedro", "minion", "4200")
usuario3 = Usuario("Marciona", "general", "4300")

# O nickname de usuário aponta para o usuário em si; Todas suas informações
usuarios = {
    usuario1.nickname : usuario1,
    usuario2.nickname : usuario2,
    usuario3.nickname : usuario3,
}
'''

# app = Flask(__name__) é a instância da classe FLask. Recebe a aplicação em si.
# O argumento da classe Flask é o nome da aplicação, assim o Flask sabe onde achar os templates e arquivos estáticos
app = Flask(__name__)
# Agora a parte do código que apresenta configurações como a secret key e o sql alchemy estão dentro do arquivo config.py
# O código abaixo agora informa de onde as configurações devem ser extraídas, no caso do arquivo config.py anteriormente criado
app.config.from_pyfile('config.py')

# Instância do banco de dados do SQLAlchemy passando a aplicação como argumento
db = SQLAlchemy(app)

# Instância da verificação CSRF para a aplicação
csrf = CSRFProtect(app)

# Instância da criptografia das senhas dos usuários
bcrypt = Bcrypt(app)

from views_game import *
from views_user import *

# Agora dentro desse if
if __name__ == '__main__':
    # Isso roda a aplicação
    # debug=True irá detectar quaisquer mudanças que ocorrerm no código e, após salvar, irá reiniciar automaticamente
    app.run(debug=True)




