from flask import render_template, request, redirect,session, flash, url_for, send_from_directory
from models import Musica, Usuario
from musica import db, app
from definicoes import recupera_imagem, deletarImagem, FormularioMusica, FormularioUsuario
import time


#--------Home-----------------------------------------------------------------


@app.route('/')
def homePage():
    
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('loginMusicas'))


    return render_template('base.html')

#--------LOGIN-----------------------------------------------------------------


@app.route('/login')
def loginMusicas():  

    form = FormularioUsuario()

    return render_template('login.html', form = form)


@app.route('/autenticar', methods=['POST',])
def autenticarUsuario():

    form = FormularioUsuario(request.form)

    
    usuario = Usuario.query.filter_by(login_usuario = form.usuario.data) .first()

    if usuario:

        if form.senha.data == usuario.senha_usuario:
           
            session['usuario_logado'] = usuario.login_usuario

            flash(f"{usuario.nome_usuario} logado com sucesso!")

            return redirect(url_for('homePage'))
        else:
    
            flash("Usuário ou senha invalido!")
            return redirect(url_for('loginMusicas'))
    else:
         
         flash("Usuário ou senha invalido!")
         return redirect(url_for('loginMusicas'))

#--------CADASTRO--------------------------------------------------------------


@app.route('/cadastro')
def cadastroMusicas():
    
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('loginMusicas'))
    
    form = FormularioMusica()
    

    return render_template('cadastra_musica.html', form = form)


@app.route('/adicionar', methods=['POST',])
def adicionarMusica(): 

    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('loginMusicas'))
    
    
    formRecebido = FormularioMusica(request.form)

    if not formRecebido.validate_on_submit():
        return redirect(url_for('cadastroMusicas'))

    nome = formRecebido.nome.data
    cantorGrupo = formRecebido.grupo.data
    genero = formRecebido.genero.data

    musica = Musica.query.filter_by(nome_musica = nome).first()

    if musica:
        flash("Esta musica ja esta cadastrada!")
        return  redirect(url_for('cadastroMusicas'))  
    
    nova_musica = Musica(nome_musica = nome, cantor_musica = cantorGrupo,
                          genero_musica = genero)
    
    db.session.add(nova_musica)
    
    db.session.commit()

    arquivo = request.files['txtArquivo']

    if arquivo:


        pasta_arquivos = app.config['UPLOAD_PASTA']

        nome_arquivo  = arquivo.filename

        nome_arquivo = nome_arquivo.split('.')

        extensao = nome_arquivo[len(nome_arquivo)-1]

        momento = time.time()

        nome_completo = f'album{nova_musica.id_musica}_{momento}.{extensao}'

        arquivo.save(f'{pasta_arquivos}/{nome_completo}')

    return redirect(url_for('listaMusicas'))

#---------LISTA----------------------------------------------------------------


@app.route('/lista')
def listaMusicas():
    
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('loginMusicas'))
       

    lista = Musica.query.order_by(Musica.id_musica)


    return render_template('lista_musicas.html', musicas = lista)


@app.route('/editar/<int:id>')
def editarMusica(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('loginMusicas'))
    
    musicaBuscada = Musica.query.filter_by(id_musica=id).first()

    form = FormularioMusica()

    form.nome.data = musicaBuscada.nome_musica
    form.grupo.data = musicaBuscada.cantor_musica
    form.genero.data = musicaBuscada.genero_musica

    album = recupera_imagem(id)
    
    return render_template('editar_musica.html',
                            musica = form, album_musica = album, id=id)


@app.route('/atualizar', methods=['POST',])
def atualizar():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('loginMusicas'))
    
    formRecebido = FormularioMusica(request.form)

    if formRecebido.validate_on_submit():
    
        musica = Musica.query.filter_by(id_musica=request.form['txtId']).first()
    
        musica.nome_musica = formRecebido.nome.data
        musica.cantor_musica = formRecebido.grupo.data
        musica.genero_musica = formRecebido.genero.data

        db.session.add(musica)

        db.session.commit()

        arquivo = request.files['txtArquivo']
    
        if arquivo:
            pasta_upload = app.config['UPLOAD_PASTA']

            nome_arquivo = arquivo.filename

            nome_arquivo = nome_arquivo.split('.')
            
            extensao = nome_arquivo[len(nome_arquivo)-1]

            
            momento = time.time()

            nome_completo = f'album{musica.id_musica}_{momento}.{extensao}'
            
            deletarImagem(musica.id_musica)

            arquivo.save(f'{pasta_upload}/{nome_completo}')

        
        flash("Musica editada com sucesso!")

    return redirect(url_for('listaMusicas'))


@app.route('/excluir/<int:id>')
def excluirMusica(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('loginMusicas'))
    
    
    Musica.query.filter_by(id_musica=id).delete()

    deletarImagem(id)

    db.session.commit()

    flash ("Musica excluida com sucesso")


    return redirect(url_for('listaMusicas'))


@app.route('/sair')
def sair():
    session['usuario_logado'] = None

    return redirect('/login')


@app.route('/uploads<nome_imagem>')
def imagem(nome_imagem):
    return send_from_directory('uploads', nome_imagem)