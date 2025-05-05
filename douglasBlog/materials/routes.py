from flask import render_template
from flask_login import login_required
from douglasBlog.helpers.permission import VerificarAdmin
from . import materials_bp


@materials_bp.route('/<int:destino>/', methods=['GET'])
def ver_materiais(destino):
    """Renderiza a página de listagem de materiais para um destino específico."""
    return render_template('materiais.html', destino=destino)

# @materials_bp.route('/download/<int:material_id>/', methods=['GET'])
# @login_required
# def download_material(material_id):
#     """Gatilho de download que também pode registrar estatísticas."""
#     # Exemplo: VerificarAdmin() se for admin-only, ou não
#     VerificarAdmin()
#     # TODO: implementar lógica de redirecionamento para URL do Supabase
#     return f"Download do material {material_id} aqui"