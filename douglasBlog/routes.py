from douglasBlog import app, db, supabase, SUPABASE_URL
from flask import render_template, url_for, request, redirect, jsonify
from flask_login import login_user, logout_user, current_user, login_required

from douglasBlog.models import User, Postagem, Material
from douglasBlog.forms import LoginForm, PostagemForm, MateriaisForm

import time
from werkzeug.utils import secure_filename

# Rota para homepage
@app.route('/')
def homepage():

    return render_template('view/index.html')

@app.route('/-<string:section>')
def homepageSection(section):

    return render_template('view/index.html', section=section)



@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    #Só permite que a função rode caso passe em todas as validações
    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    print(form.errors)

    return render_template('login/login.html', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))





@app.route('/admin/douglas-blog/dashboard/')
@login_required
def dashboard():


    return render_template('admin/dashboard.html')


@app.route('/admin/douglas-blog/posts/criar/', methods=['GET', 'POST'])
@login_required
def criarPosts():
    if current_user.admin == False:
        return redirect(url_for('homepage'))
    form = PostagemForm()
    
    if form.validate_on_submit():
        form.save(current_user.id)
        return redirect(url_for('listaPosts'))

    return render_template('admin/criar/criar-posts.html', form=form)


@app.route('/api/upload-image-ckeditor', methods=['POST'])
@login_required
def upload_image_ckeditor():
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
def criarMateriais():
    form = MateriaisForm()

    if form.validate_on_submit():
        form.save()
        return redirect(url_for('dashboard'))

    return render_template('admin/criar/criar-materiais.html', form=form)


# ------------------------------------------------------------- #
        # VIEW/
            # / MATERIAIS

                    # MATERIAIS.HTML
@app.route('/materiais/turmas/<int:turma>/')
def materiaisTurmas(turma):
    
    return render_template('view/materiais/materiais.html')


def converter_lista_materiais_para_dict(material):

    return {
        "id": material.id,
        "destino": material.destino,
        "titulo": material.titulo,
        "aula": material.aula,
        "mapa_mental": material.mapa_mental,
        "lista_exercicios": material.lista_exercicios,
        "data_criacao": material.data_criacao,
    }


@app.route('/api/get/lista-materiais/<int:destino>', methods=['GET'])
def api_get_listaMateriais(destino):
    try:
        # extraindo os materiais
        materiais_query = Material.query.filter_by(destino=destino)
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


# Função para serializar o objeto Postagem para formato JSON
def converter_lista_post_para_dict(post):
    if post.imagem == None:
        url_imagem = url_for('static', filename='media/templates/oba-banner.jpg')
    else:
        url_imagem = post.imagem

    return {
        "id": post.id,
        "titulo": post.titulo,
        "imagem": url_imagem,
        "conteudo": post.conteudoResumo(),
        "link": url_for('verPost', post_titulo=post.titulo, post_id=post.id)
    }


@app.route('/api/get/lista-posts', methods=['GET'])
def api_get_listaPosts():
    try:
        # Parametros para carregamento de posts na pagina:
        pagina = int(request.args.get('page', 1)) # Recebe o número da página pelo cabeçalho
        posts_por_pagina = 8 # Número de posts carregados na página
        inicio = (pagina - 1) * posts_por_pagina # Calcula o primeiro post carregado (ex: 1 = 0, 2 = 51)

        # Extraindo os posts
        posts_carregados = Postagem.query.offset(inicio).limit(posts_por_pagina).all() # Fatia query, enviando apenas o necessário
        posts_carregados_dict = [converter_lista_post_para_dict(post) for post in posts_carregados] # Converte para dict


        # Contando total de posts
        posts_total = Postagem.query.count()


        # Criando a resposta JSON
        response = jsonify(posts_carregados_dict) # Converte lista de posts em json
        response.headers['X-Total-Count'] = posts_total # Envia para o cabeçalho o total de posts

        return response

    except Exception as e:
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