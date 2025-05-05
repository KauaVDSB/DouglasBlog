from flask import jsonify, request
from sqlalchemy import desc
from douglasBlog.models import Material
from . import materials_bp


def _serialize_material(material):
    """Converte entidade Material em dict para JSON."""
    return {
        'id': material.id,
        'destino': material.destino,
        'titulo': material.titulo,
        'aula': material.aula,
        'resumo': material.resumo,
        'lista_exercicios': material.lista_exercicios,
        'data_criacao': material.data_criacao.isoformat()
    }

@materials_bp.route('/api/get/lista-materiais/<int:destino>', methods=['GET'])
def api_lista_materiais(destino):
    """Retorna JSON com lista paginada de materiais para um destino."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    query = Material.query.filter_by(destino=destino).order_by(desc(Material.data_criacao))
    total = query.count()
    materiais = query.offset((page - 1) * per_page).limit(per_page).all()

    data = [_serialize_material(m) for m in materiais]
    response = jsonify(data)
    response.headers['X-Total-Count'] = total
    return response

@materials_bp.route('/api/get/ver-material/<int:material_id>', methods=['GET'])
def api_ver_material(material_id):
    """Retorna JSON com detalhes de um material específico."""
    material = Material.query.get_or_404(material_id)
    return jsonify(_serialize_material(material))