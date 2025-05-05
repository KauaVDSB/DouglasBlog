from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required

from douglasBlog import ACESSO_CADASTRO, ACESSO_LOGIN
from douglasBlog.forms import UserForm, LoginForm
# Blueprint definition
auth_bp = Blueprint(
    "auth", __name__, template_folder="templates", static_folder="static"
)



@auth_bp.route("/cadastroooooooo/<string:validacao>", methods=["GET", "POST"])
def cadastro(validacao):
    if validacao != ACESSO_CADASTRO:
        return redirect(url_for("homepage"))

    form = UserForm()

    if form.validate_on_submit():
        form.save()
        return redirect(url_for("homepage"))

    return render_template("login/cadastro.html", form=form)


@auth_bp.route("/login/", methods=["GET", "POST"])
def login():
    if request.args.get("acesso") != ACESSO_LOGIN:
        return redirect(url_for("homepage"))

    form = LoginForm()

    # Só permite que a função rode caso passe em todas as validações e seja admin
    if form.validate_on_submit():
        user = form.login()
        if user:
            login_user(user, remember=True)
            return redirect(url_for("dashboard"))

    return render_template(
        "login/login.html", form=form, ACESSO_CADASTRO=ACESSO_CADASTRO
    )


@auth_bp.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

