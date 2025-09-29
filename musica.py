from flask import Flask, render_template, request, redirect,session, flash, url_for

from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


app.secret_key = 'thalescostaqueiroga'



app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'domingo1',
        servidor = 'localhost',
        database = 'playmusica'
    )  

db = SQLAlchemy(app)   

class Musica(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nome_musica = db.Column(db.String(50), nullable = False)
    cantor_musica = db.Colum(db.String(50), nullable = False)
    genero_musica = db.Colum(db.String(20), nullable = False)


    def __repr__(self):
        return '<Name %r>' %self.name


@app.route('/login')
def loginMusicas():  

    return render_template('login.html')

@app.route('/autenticar', methods=['POST',])
def autenticarUsuario():

    if request.form['txtLogin'] in usuarios:

        usuarioEncontrado = usuarios[request.form['txtLogin']]
        
        if request.form['txtSenha'] == usuarioEncontrado.senha:

            session['usuario_logado'] = request.form['txtLogin']

            flash(f"{usuarioEncontrado.nome} logado com sucesso!")

            return redirect(url_for('homePage'))
        else:
            flash("Usuário ou senha invalido!")
            return redirect(url_for('loginMusicas'))
    else:
         
         flash("Usuário ou senha invalido!")
         return redirect(url_for('loginMusicas'))
    

@app.route('/')
def homePage():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('loginMusicas'))


    return render_template('base.html')


@app.route('/lista')
def listaMusicas():   
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('loginMusicas'))


    return render_template('lista_musicas.html', musicas = lista)


@app.route('/cadastro')
def cadastroMusicas():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('loginMusicas'))
    

    return render_template('cadastra_musica.html')


@app.route('/adicionar', methods=['POST',])
def adicionarMusica(): 
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('loginMusicas'))

    
    nome = request.form['txtNome']
    cantorGrupo = request.form['txtCantorGrupo']
    genero = request.form['txtGenero']

    novaMusica = Musica(nome, cantorGrupo, genero)

    lista.append(novaMusica)

   
    return redirect(url_for('ListaMusicas'))

@app.route('/sair')
def sair():
    session['usuario_logado'] = None

    return redirect('/login')
    

app.run(debug=True)