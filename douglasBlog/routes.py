from douglasBlog import app, db
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required

from douglasBlog.models import User
from douglasBlog.forms import LoginForm

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