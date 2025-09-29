from flask import Flask, render_template, request, redirect,session, flash, url_for

app = Flask(__name__)

class Musica:
    def __init__(self, nome, cantorGrupo, genero):

        self.nome = nome 
        self.cantorGrupo = cantorGrupo
        self.genero = genero


app.secret_key = 'thalescostaqueiroga'


musicas01 = Musica('Lobo Azul', 'Zé Neto & Cristiano', 'Sertanejo')
musicas02 = Musica('Solidão', 'Ana Carolina', 'MP3')
musicas03 = Musica('Solidão', 'Roupa Nova', 'Pop Rock')

lista = [musicas01, musicas02,musicas03]

class Usuario:
    def __init__(self, nome, login, senha):
        self.nome = nome
        self.login = login
        self.senha = senha
         

usuario01 = Usuario("Thales Costa Queiroga", "thales.queiroga", "domingo1")
usuario02 = Usuario("Joao Pedro", "joao.pedro", "123321")
usuario03 = Usuario("Lorhayne Crystina", "lorhayne.crystina", "1234")

usuarios = {
    usuario01.login : usuario01,
    usuario02.login : usuario02,
    usuario03.login : usuario03
}
        

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