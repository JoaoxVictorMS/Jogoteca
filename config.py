import os
# Senha mestre
SECRET_KEY = 'santosfc'

# URI que realiza a conexão com o banco de dados MySQL
# Colocando a barra invertida, faz possível colocar o código em baixo dela, como mostrado abaixo
SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        usuario='root',
        senha='',
        servidor='localhost',
        database='jogoteca'
    )
# Referência do arquivo
#dirname devolve o caminho do diretório jogoteca
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'