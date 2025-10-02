import os

SECRET_KEY = 'thalescostaqueiroga'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'domingo1',
        servidor = 'localhost',
        database = 'playmusica'
    ) 

UPLOAD_PASTA = os.path.dirname(os.path.abspath(__file__)) + '/uploads'