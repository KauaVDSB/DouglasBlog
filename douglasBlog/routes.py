from douglasBlog import app, db, supabase, SUPABASE_URL
from flask import render_template, url_for, request, redirect, jsonify, session, flash
from flask_login import login_user, logout_user, current_user, login_required

from sqlalchemy import desc, func
from douglasBlog.models import Postagem, Material, User
from douglasBlog.forms import LoginForm, PostagemForm, MateriaisForm, UserForm
from douglasBlog.utils import VerificarAdmin

from time import time
import re
from werkzeug.utils import secure_filename


# Rota para homepage
@app.route('/')
def homepage():

    return render_template('view/index.html')

@app.route('/-<string:section>')
def homepageSection(section):

    return render_template('view/index.html', section=section)




@app.route('/cadastroooooooo/<string:validacao>', methods=['GET', 'POST'])
def cadastro(validacao):
    if validacao != 'acesso_confirmado': # <!-- VARIAVEL DE AMBIENTE -->
        return redirect(url_for('homepage'))
    
    form = UserForm()

    if form.validate_on_submit():
        form.save()
        return redirect(url_for('homepage'))

    return render_template('login/cadastro.html', form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.args.get('acesso') == 'douglas': # <!-- VARIAVEL DE AMBIENTE -->
        session['acesso_douglas'] = True
        return redirect(url_for('login'))

    if not session.get('acesso_douglas'):
        return redirect(url_for('homepage'))

    form = LoginForm()

    #Só permite que a função rode caso passe em todas as validações e seja admin
    if form.validate_on_submit():
        user = form.login()
        if user:
            login_user(user, remember=True)
            return redirect(url_for('dashboard'))

    return render_template('login/login.html', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))





@app.route('/admin/douglas-blog/dashboard/')
@login_required
def dashboard():
    VerificarAdmin()

    return render_template('admin/dashboard.html')


@app.route('/admin/douglas-blog/posts/criar/', methods=['GET', 'POST'])
@login_required
def criarPosts():
    VerificarAdmin()

    form = PostagemForm()
    
    if form.validate_on_submit():
        form.save(current_user.id)
        return redirect(url_for('listaPosts'))

    return render_template('admin/criar/criar-posts.html', form=form)


@app.route('/admin/douglas-blog/posts/editar/<int:post_id>', methods=['GET', 'POST'])
@login_required
def editarPost(post_id):
    VerificarAdmin()

    post = Postagem.query.get_or_404(post_id)

    form = PostagemForm(
        titulo = post.titulo,
        imagem = post.imagem,
        conteudo = post.conteudo
    )

    if form.validate_on_submit():
        try:
            form.update(post)
            db.session.commit()
            # print('Postagem editada com sucesso!') #Trocar por jsonify para utilizar Swal.fire
            return redirect(url_for('listaPosts'))
        except Exception as e:
            db.session.rollback()
            # print(f'Falha ao editar postagem. Erro: {e}') #Trocar por jsonify para utilizar Swal.fire
            return redirect(url_for('dashboard'))

    return render_template('admin/editar/editar-post.html', form=form, post=post)

@app.route('/admin/douglas-blog/posts/deletar/<int:post_id>', methods=['DELETE'])
@login_required
def deletarPost(post_id):
    VerificarAdmin()

    post = Postagem.query.get_or_404(post_id)

    delete = PostagemForm()

    return delete.delete(post)




@app.route('/api/upload-image-ckeditor', methods=['POST'])
@login_required
def upload_image_ckeditor():
    VerificarAdmin()

    file = request.files.get('upload')
    if not file:
        return jsonify({'error': 'Nenhum arquivo enviado.'}), 400
    
    unique_filename = f"{int(time.time())}_{secure_filename(file.filename)}"
    caminho_arquivo = f"post-files/{unique_filename}"
    file_bytes = file.read()

    supabase.storage.from_('post-files').upload(caminho_arquivo, file_bytes)

    url_imagem = f"{SUPABASE_URL}/storage/v1/object/public/post-files/post-files/{unique_filename}"

    return jsonify({'url': url_imagem})


@app.route('/admin/douglas-blog/materiais/criar/', methods=['GET', 'POST'])
@login_required
def criarMateriais():
    VerificarAdmin()

    form = MateriaisForm()

    if form.validate_on_submit():
        form.save()
        return redirect(url_for('dashboard'))

    return render_template('admin/criar/criar-materiais.html', form=form)



@app.route('/admin/douglas-blog/materiais/editar/<int:material_id>', methods=['GET', 'POST'])
@login_required
def editar_material(material_id):
    VerificarAdmin()

    material = Material.query.get_or_404(material_id)

    form = MateriaisForm(
        titulo = material.titulo,
        aula = material.aula,
        resumo = material.resumo,
        lista_exercicios = material.lista_exercicios,
        destino = material.destino
    )

    if form.validate_on_submit():
        form.update(material)
        db.session.commit()
        destino = Material.query.with_entities(
            Material.destino).filter_by(id=material_id).scalar()
        flash("Material editado com sucesso!")
        return redirect(url_for('verMateriais', destino=int(destino)))
    
    return render_template('admin/editar/editar-material.html', form=form, material=material)


@app.route('/admin/douglas-blog/materiais/deletar/<int:material_id>', methods=['DELETE'])
@login_required
def deletar_material(material_id):
    VerificarAdmin()

    material = Material.query.get_or_404(material_id)

    delete = MateriaisForm()

    return delete.delete(material)
# ------------------------------------------------------------- #
        # VIEW/
            # / MATERIAIS

                    # MATERIAIS.HTML
@app.route('/materiais/<int:destino>/')
def verMateriais(destino):
    
    return render_template('view/materiais/materiais.html')


def converter_lista_materiais_para_dict(material):

    return {
        "id": material.id,
        "destino": material.destino,
        "titulo": material.titulo,
        "aula": material.aula,
        "resumo": material.resumo,
        "lista_exercicios": material.lista_exercicios,
        "data_criacao": material.data_criacao,
    }


@app.route('/api/get/lista-materiais/<int:destino>', methods=['GET'])
def api_get_listaMateriais(destino):
    try:
        # extraindo os materiais
        materiais_query = Material.query.filter_by(destino=destino).order_by(desc(Material.data_criacao))
        materiais = list(materiais_query)  # Garante que seja uma lista
        
        materiais_dict = [converter_lista_materiais_para_dict(material) for material in materiais]
        materiais_total = len(materiais_dict)

        # Criando resposta JSON
        response = jsonify({
            "materiais": materiais_dict,
            "total": materiais_total
        })
        response.headers['X-Total-Count'] = materiais_total
        return response
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500





# /POSTS/

                # /LISTA-POSTS.HTML
@app.route('/posts/lista/')
def listaPosts():

    return render_template('view/posts/lista-posts.html')


def converter_entities_lista_post_para_dict(id, titulo, imagem, conteudo):
    if imagem is None:
        url_imagem = url_for('static', filename='media/templates/oba-banner.jpg')
    else:
        url_imagem = imagem

    post_conteudo = re.sub(r'<[^>]*?>', '', conteudo or '')
    if len(post_conteudo) > 60:
        resumo = f"{post_conteudo[:37]}..."
    else:
        resumo = post_conteudo

    return {
        "id": id,
        "titulo": titulo,
        "imagem": url_imagem,
        "conteudo": resumo,
        "link": url_for('verPost', post_titulo=titulo, post_id=id)
    }


@app.route('/api/get/lista-posts', methods=['GET'])
def api_get_listaPosts():
    try:
        # Parametros para carregamento de posts na pagina:
        pagina = request.args.get('page', 1) # Recebe o número da página pelo cabeçalho

        try:
            pagina = int(pagina)
            if pagina < 1:
                pagina =1
        except ValueError:
            pagina = 1

        posts_por_pagina = 8 # Número de posts carregados na página
        inicio = (pagina - 1) * posts_por_pagina # Calcula o primeiro post carregado (ex: 1 = 0, 2 = 51)

        #PERFORMANCE
        # t0 = time()

        # Extraindo os posts
        posts_carregados = db.session.query(
            Postagem.id,
            Postagem.titulo,
            Postagem.imagem,
            Postagem.conteudo
        ).order_by(
            desc(Postagem.data_postagem)
        ).offset(inicio).limit(posts_por_pagina).all() # Fatia query, enviando apenas o necessário

        #PERFORMANCE
        # t1 = time()


        posts_carregados_dict = [
            converter_entities_lista_post_para_dict(id, titulo, imagem, conteudo)
            for id, titulo, imagem, conteudo in posts_carregados
        ]

        # Contando total de posts
        posts_total = db.session.query(func.count(Postagem.id)).scalar()

        # t2 = time()

        # Logs de desempenho de DEBUG PERFORMANCE
        # print(f"Tempo consulta com with_entities: {(t1 - t0)*1000:.2f} ms")
        # print(f"Tempo total (com contagem): {(t2 - t0)*1000:.2f} ms")


        # Criando a resposta JSON
        response = jsonify(posts_carregados_dict) # Converte lista de posts em json
        response.headers['X-Total-Count'] = posts_total # Envia para o cabeçalho o total de posts

        return response

    except Exception as e:
        flash(f"❌ Erro ao buscar posts: {e}")
        return jsonify({"error": str(e)}), 500 # Retorna erro como json em caso de falha.
    




                # VIEW/POST.HTML
@app.route('/posts/view/<string:post_titulo>/<int:post_id>/')
def verPost(post_titulo, post_id):
    post_detail = Postagem.query.get(post_id)

    return render_template('view/posts/post.html', post=post_detail)


# Função para serializar o objeto Postagem para formato JSON
def converter_post_para_dict(post):
    return {
        "id": post.id,
        "titulo": post.titulo,
        "conteudo": post.conteudo,
        "data_postagem": post.data_resumo(),
        "user_id": post.user_id
    }


@app.route('/api/get/ver-post/<int:id>')
def api_get_verPost(id):
    post = Postagem.query.get_or_404(id)
    post_dict = converter_post_para_dict(post)

    # Resposta JSON
    response = jsonify(post_dict)

    return response