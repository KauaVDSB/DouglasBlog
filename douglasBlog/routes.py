from douglasBlog import app, db
from flask import render_template, url_for, request, redirect, jsonify
from flask_login import login_user, logout_user, current_user, login_required

from douglasBlog.models import User, Postagem
from douglasBlog.forms import LoginForm, PostagemForm

# Rota para homepage
@app.route('/')
def homepage():

    return render_template('index.html')



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


@app.route('/criar-postagem/', methods=['GET', 'POST'])
@login_required
def criarPostagem():
    if current_user.admin == False:
        return redirect(url_for('homepage'))
    form = PostagemForm()

    if form.validate_on_submit():
        form.save(current_user.id)
        return redirect(url_for('homepage'))

    return render_template('admin/posts/criar-postagem.html', form=form)

@app.route('/get-posts/')
def getDados():
    posts = Postagem.query.all()

    return jsonify([{"autor": post.user.nome, "titulo": post.titulo, "conteudo": post.conteudo} for post in posts])