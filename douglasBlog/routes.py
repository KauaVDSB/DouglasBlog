from douglasBlog import app, db
from flask import render_template, url_for, request, redirect, jsonify
from flask_login import login_user, logout_user, current_user, login_required

from douglasBlog.models import User, Postagem
from douglasBlog.forms import LoginForm, PostagemForm

# Rota para homepage
@app.route('/')
def homepage():

    return render_template('view/index.html')

@app.route('/#<string:section>')
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


@app.route('/admin/douglas-blog/posts/admin/criar/', methods=['GET', 'POST'])
@login_required
def criarPosts():
    if current_user.admin == False:
        return redirect(url_for('homepage'))
    form = PostagemForm()
    
    if form.validate_on_submit():
        form.save(current_user.id)
        return redirect(url_for('homepage'))

    return render_template('admin/criar-posts.html', form=form)


@app.route('/posts/lista/')
def listaPosts():

    posts = Postagem.query.all()

    return render_template('view/lista-posts.html', posts=posts)

# Função para serializar o objeto Postagem para formato JSON
def post_to_dict(post):
    return {
        "id": post.id,
        "titulo": post.titulo,
        "conteudo": post.conteudoResumo()
    }

@app.route('/api/get/lista-posts', methods=['GET'])
def api_get_listaPosts():
    try:
        # Parametros para carregamento de posts na pagina:
        pagina = int(request.args.get('page', 1)) # Recebe o número da página pelo cabeçalho
        posts_por_pagina = 5 # Número de posts carregados na página
        inicio = (pagina - 1) * posts_por_pagina # Calcula o primeiro post carregado (ex: 1 = 0, 2 = 51)

        # Extraindo os posts
        posts_carregados = Postagem.query.offset(inicio).limit(posts_por_pagina).all() # Fatia query, enviando apenas o necessário
        posts_carregados_dict = [post_to_dict(post) for post in posts_carregados] # Converte para dict


        # Contando total de posts
        posts_total = Postagem.query.count()


        # Criando a resposta JSON
        response = jsonify(posts_carregados_dict) # Converte lista de posts em json
        response.headers['X-Total-Count'] = posts_total # Envia para o cabeçalho o total de posts

        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500 # Retorna erro como json em caso de falha.
    




@app.route('/get-posts/')
def getDados():
    posts = Postagem.query.all()

    return jsonify([{"autor": post.user.nome, "titulo": post.titulo, "conteudo": post.conteudo} for post in posts])