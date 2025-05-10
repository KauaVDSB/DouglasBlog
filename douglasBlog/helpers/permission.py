from flask import abort
from flask_login import current_user


def VerificarAdmin():
    """
    Se o usuário atual não for admin, redireciona para a homepage com flash
    e interrompe a execução. Caso contrário, retorna True.
    """
    if not current_user.admin:
        abort(403)
    return True
