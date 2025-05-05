from flask import Blueprint, url_for, request, jsonify, flash
from sqlalchemy import func, desc
from douglasBlog import db
from douglasBlog.models import Postagem
from douglasBlog.exceptions import GetAPIError

# Blueprint definition
blog_bp = Blueprint(
    "blog", __name__, template_folder="templates/blog", static_folder="static/blog"
)

# ---------- API Endpoints ----------


def _serialize_post(post):
    """Converte entidade Postagem em dict para JSON."""
    return {
        "id": post.id,
        "titulo": post.titulo,
        "imagem": post.imagem
        or url_for("static", filename="media/templates/oba-banner.jpg"),
        "conteudo": (post.conteudo or "")[:70],
        "link": url_for("blog.ver_post", post_titulo=post.titulo, post_id=post.id),
    }


# @blog_bp.route("/api/get/lista-posts", methods=["GET"])
# def api_lista_posts():
#     """Retorna JSON com lista de posts paginada e cabeçalho X-Total-Count."""
#     # Parâmetros de paginação
#     page = request.args.get("page", 1, type=int)
#     page = max(page, 1)
#     per_page = 8

#     # Query principal
#     query = db.session.query(Postagem).order_by(desc(Postagem.data_postagem))
#     total = query.count()
#     posts = query.offset((page - 1) * per_page).limit(per_page).all()

#     data = [_serialize_post(p) for p in posts]
#     response = jsonify(data)
#     response.headers["X-Total-Count"] = total
#     return response

@blog_bp.route("/api/get/lista-posts", methods=["GET"])
def api_get_listaPosts():
    try:
        # Parametros para carregamento de posts na pagina:
        pagina = request.args.get("page", 1)  # Recebe o número da página pelo cabeçalho

        try:
            pagina = int(pagina)
            pagina = max(pagina, 1)
        except ValueError:
            pagina = 1

        posts_por_pagina = 8  # Número de posts carregados na página
        inicio = (
            pagina - 1
        ) * posts_por_pagina  # Calcula o primeiro post carregado (ex: 1 = 0, 2 = 51)

        # PERFORMANCE
        # t0 = time()

        # Extraindo os posts
        posts_carregados = (
            db.session.query(
                Postagem.id, Postagem.titulo, Postagem.imagem, Postagem.conteudo
            )
            .order_by(desc(Postagem.data_postagem))
            .offset(inicio)
            .limit(posts_por_pagina)
            .all()
        )  # Fatia query, enviando apenas o necessário

        # PERFORMANCE
        # t1 = time()

        posts_carregados_dict = [
            _serialize_post(id, titulo, imagem, conteudo)
            for id, titulo, imagem, conteudo in posts_carregados
        ]

        # Contando total de posts
        posts_total = db.session.query(
            func.count(Postagem.id)  # pylint: disable=not-callable
        ).scalar()

        # t2 = time()

        # Logs de desempenho de DEBUG PERFORMANCE
        # print(f"Tempo consulta com with_entities: {(t1 - t0)*1000:.2f} ms")
        # print(f"Tempo total (com contagem): {(t2 - t0)*1000:.2f} ms")

        # Criando a resposta JSON
        response = jsonify(posts_carregados_dict)  # Converte lista de posts em json
        response.headers["X-Total-Count"] = (
            posts_total  # Envia para o cabeçalho o total de posts
        )

        return response

    except GetAPIError as e:
        flash(f"❌ Erro ao buscar posts: {e}")
        return (
            jsonify({"error": str(e)}),
            500,
        )  # Retorna erro como json em caso de falha.



@blog_bp.route("/api/get/ver-post/<int:post_id>", methods=["GET"])
def api_ver_post(post_id):
    """Retorna JSON com dados completos de um post."""
    post = Postagem.query.get_or_404(post_id)
    return jsonify(
        {
            "id": post.id,
            "titulo": post.titulo,
            "conteudo": post.conteudo,
            "data_postagem": post.data_resumo(),
            "user_id": post.user_id,
        }
    )
