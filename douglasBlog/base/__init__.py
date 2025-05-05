from flask import Blueprint

base_bp = Blueprint(
    "base",  # nome do blueprint
    __name__,  # pacote onde ele vive
    template_folder="templates",
    static_folder="static",
)

# Importa rotas e APIs para registro automático
from . import routes # noqa: F401,E402  #pylint: disable=unused-import
