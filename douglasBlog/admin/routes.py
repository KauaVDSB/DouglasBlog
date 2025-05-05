from time import time

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from douglasBlog import db, SUPABASE_URL, supabase_client
from douglasBlog.models import Postagem, Material
from douglasBlog.forms import PostagemForm, MateriaisForm
from douglasBlog.helpers.permission import VerificarAdmin
from douglasBlog.exceptions import QueryObjectManagementError

# Blueprint definition
admin_bp = Blueprint(
    "admin", __name__, template_folder="templates", static_folder="static"
)


@admin_bp.route("/admin/douglas-blog/dashboard/")
@login_required
def dashboard():
    VerificarAdmin()

    return render_template("dashboard.html")


@admin_bp.route("/admin/douglas-blog/posts/criar/", methods=["GET", "POST"])
@login_required
def criar_posts():
    VerificarAdmin()

    form = PostagemForm()

    if form.validate_on_submit():
        form.save(current_user.id)
        return redirect(url_for("blog.lista_posts"))

    return render_template("criar/criar-posts.html", form=form)


@admin_bp.route("/admin/douglas-blog/posts/editar/<int:post_id>", methods=["GET", "POST"])
@login_required
def editar_post(post_id):
    VerificarAdmin()

    post = Postagem.query.get_or_404(post_id)

    form = PostagemForm(titulo=post.titulo, imagem=post.imagem, conteudo=post.conteudo)

    if form.validate_on_submit():
        try:
            form.update(post)
            db.session.commit()
            flash(
                "Postagem editada com sucesso!"
            )  # Trocar por jsonify para utilizar Swal.fire
            return redirect(url_for("blog.lista_posts"))
        except QueryObjectManagementError as e:
            db.session.rollback()
            flash(
                f"Falha ao editar postagem. Erro: {e}"
            )  # Trocar por jsonify para utilizar Swal.fire
            return redirect(url_for("dashboard"))

    return render_template("editar/editar-post.html", form=form, post=post)


@admin_bp.route("/admin/douglas-blog/posts/deletar/<int:post_id>", methods=["DELETE"])
@login_required
def deletar_post(post_id):
    VerificarAdmin()

    post = Postagem.query.get_or_404(post_id)

    delete = PostagemForm()

    return delete.delete(post)


@admin_bp.route("/api/upload-image-ckeditor", methods=["POST"])
@login_required
def upload_image_ckeditor():
    VerificarAdmin()

    file = request.files.get("upload")
    if not file:
        return jsonify({"error": "Nenhum arquivo enviado."}), 400

    unique_filename = f"{int(time.time())}_{secure_filename(file.filename)}"
    caminho_arquivo = f"post-files/{unique_filename}"
    file_bytes = file.read()

    supabase_client.storage.from_("post-files").upload(caminho_arquivo, file_bytes)

    url_imagem = f"{SUPABASE_URL}/storage/v1/object/public/post-files/post-files/{unique_filename}"

    return jsonify({"url": url_imagem})


@admin_bp.route("/admin/douglas-blog/materiais/criar/", methods=["GET", "POST"])
@login_required
def criar_materiais():
    VerificarAdmin()

    form = MateriaisForm()

    if form.validate_on_submit():
        form.save()
        return redirect(url_for("dashboard"))

    return render_template("criar/criar-materiais.html", form=form)


@admin_bp.route(
    "/admin/douglas-blog/materiais/editar/<int:material_id>", methods=["GET", "POST"]
)
@login_required
def editar_material(material_id):
    VerificarAdmin()

    material = Material.query.get_or_404(material_id)

    form = MateriaisForm(
        titulo=material.titulo,
        aula=material.aula,
        resumo=material.resumo,
        lista_exercicios=material.lista_exercicios,
        destino=material.destino,
    )

    if form.validate_on_submit():
        form.update(material)
        db.session.commit()
        destino = (
            Material.query.with_entities(Material.destino)
            .filter_by(id=material_id)
            .scalar()
        )
        flash("Material editado com sucesso!")
        return redirect(url_for("verMateriais", destino=int(destino)))

    return render_template(
        "admin/editar/editar-material.html", form=form, material=material
    )


@admin_bp.route(
    "/admin/douglas-blog/materiais/deletar/<int:material_id>", methods=["DELETE"]
)
@login_required
def deletar_material(material_id):
    VerificarAdmin()

    material = Material.query.get_or_404(material_id)

    delete = MateriaisForm()

    return delete.delete(material)
