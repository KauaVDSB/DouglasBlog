from flask import Blueprint, render_template
from douglasBlog.models import Postagem

# Blueprint definition
blog_bp = Blueprint(
    "blog", __name__, template_folder="templates", static_folder="static"
)

# ---------- Page Views ----------


@blog_bp.route("/posts/lista/", methods=["GET"])
def lista_posts():
    """Renderiza a página com listagem de posts."""
    return render_template("posts/lista-posts.html")


@blog_bp.route("/posts/view/<string:post_titulo>/<int:post_id>/", methods=["GET"])
def ver_post(post_titulo, post_id):
    """Renderiza página de detalhe de um post."""
    post = Postagem.query.get_or_404(post_id)
    return render_template("posts/post.html", post=post)
