from flask import redirect, url_for, flash
from flask_login import current_user


def VerificarAdmin():
    """
    Se o usuário atual não for admin, redireciona para a homepage com flash
    e interrompe a execução. Caso contrário, retorna True.
    """
    if not current_user.admin:
        flash("Você não tem permissão para realizar essa ação.")
        return redirect(url_for("homepage"))
    flash("Acesso concedido.")
    return True
