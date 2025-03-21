from douglasBlog import app, db
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required

from douglasBlog.models import User
from douglasBlog.forms import UserForm

# Rota para homepage
@app.route('/')
def homepage():

    flash('lhe amo, meu bem <3', 'amor')

    return render_template('index.html')


@app.route('/login/')
def login():

    return render_template('login/login.html')