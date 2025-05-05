from flask import Blueprint

admin_bp = Blueprint(
    "admin",  # nome do blueprint
    __name__,  # pacote onde ele vive
    template_folder="templates",
    static_folder="static",
)

# Importa rotas e APIs para registro automático
from . import routes, api  # noqa: F401,E402  #pylint: disable=unused-import
