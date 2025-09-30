from flask import render_template, request, redirect,session, flash, url_for
from models import Musica, Usuario
from musica import db, app


@app.route('/editar/<int:id>')
def editarMusica(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('loginMusicas'))
    
    musicaBuscada = Musica.query.filter_by(id_musica=id).first()
    
    return render_template('editar_musica.html', musica = musicaBuscada)


@app.route('/atualizar', methods=['POST',])
def atualizar():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('loginMusicas'))
    
    musica = Musica.query.filter_by(id_musica=request.form['txtId']).first()
    
    musica.nome_musica = request.form['txtNome']
    musica.cantor_musica = request.form['txtCantorGrupo']
    musica.genero_musica = request.form['txtGenero']

    db.session.add(musica)

    db.session.commit()
    return redirect(url_for('listaMusicas'))

@app.route('/login')
def loginMusicas():  

    return render_template('login.html')


@app.route('/autenticar', methods=['POST',])
def autenticarUsuario():

    usuario = Usuario.query.filter_by(login_usuario = request.form['txtLogin']).first()

    if usuario:

        if request.form['txtSenha'] == usuario.senha_usuario:
           
            session['usuario_logado'] = request.form['txtLogin']

            flash(f"{usuario.nome_usuario} logado com sucesso!")

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
       

    lista = Musica.query.order_by(Musica.id_musica)

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

    musica = Musica.query.filter_by(nome_musica = nome).first()

    if musica:
        flash("Esta musica ja esta cadastrada!")
        return  redirect(url_for('cadastroMusicas'))  
    
    nova_musica = Musica(nome_musica = nome, cantor_musica = cantorGrupo,
                          genero_musica = genero)
    
    db.session.add(nova_musica)
    
    db.session.commit()

    return redirect(url_for('listaMusicas'))


@app.route('/sair')
def sair():
    session['usuario_logado'] = None

    return redirect('/login')