import os
#Importa a aplicação
from jogoteca import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField

class FormularioJogo(FlaskForm):
   # StringField() recebe a label dentro do input e a forma de validação do mesmo
   # Neste caso ele valida pelo tamanho da string, pois é um campo do tipo string(varchar), que é o mesmo do banco de dados
   # Além disso ele precisa do dado, pro isso o DataRequired()
   nome = StringField('Nome do jogo', [validators.DataRequired(), validators.Length(min=1, max=50)])
   categoria = StringField('Categoria', [validators.DataRequired(), validators.Length(min=1, max=40)])
   console = StringField('Console', [validators.DataRequired(), validators.Length(min=1, max=20)])
   salvar = SubmitField('Salvar')

class FormularioUsuario(FlaskForm):
   nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=8)])
   senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
   login = SubmitField('Login')

def recupera_imagem(id):
    ''' Recupera a imagem referente ao jogo específico  '''
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        # Mudando de "==" para "in" pois agora cada nome é único, logo ele sempre verifica se o id da capa esta CONTIDO no nome do arquivo
        if f'capa{id}' in nome_arquivo:
         return nome_arquivo
        
    return 'PLACEHOLDER =.jpg'

def deleta_arquivo(id):
   ''' Deleta alguma imagem específica '''
   arquivo = recupera_imagem(id)
   if arquivo != 'PLACEHOLDER =.jpg':
      # Dá o caminho para a pasta que estão as imagens para então poder deletar
      os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))


