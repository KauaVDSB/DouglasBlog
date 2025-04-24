import time

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    TextAreaField,
    SelectField,
    FileField,
)

# Para validar email, baixar biblioteca email_validator
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask import request, flash, jsonify

from werkzeug.utils import secure_filename

from douglasBlog import db, bcrypt, supabase, SUPABASE_URL
from douglasBlog.models import User, Postagem, Material
from douglasBlog.exceptions import (
    AuthenticationError,
    ResourceNotSentError,
    ResourceNotFoundError,
    SupabaseManagementFileError,
    QueryObjectManagementError,
    EncryptationFailureError,
)


class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    btnSubmit = SubmitField("Entrar")

    def login(self):
        user = User.query.filter_by(email=self.email.data).first()

        if not user:
            raise ResourceNotFoundError("Usuário não encontrado.")
        if not user.admin:
            raise PermissionError("Usuário não é um admnistrador. Acesso negado.")
        if not bcrypt.check_password_hash(user.senha, self.senha.data.encode("utf-8")):
            raise AuthenticationError("Senha incorreta.")

        # print("Usuário logado com sucesso!") #DEBUG
        return user


class PostagemForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired()])
    imagem = FileField("Imagem")
    conteudo = TextAreaField("Conteúdo")
    btnSubmit = SubmitField("Publicar")

    @staticmethod
    def generate_unique_filename(filename):
        """Gera um nome único para o arquivo."""
        return f"{int(time.time())}_{secure_filename(filename)}"

    def get_url_imagem(self):
        imagem = self.imagem.data
        url_imagem = None

        if imagem and imagem.filename:
            unique_filename = self.generate_unique_filename(imagem.filename)

            # Envia para o Supabase Storage
            caminho_arquivo = f"post-files/{unique_filename}"
            imagem_bytes = imagem.read()

            # Upload
            supabase.storage.from_("post-files").upload(
                caminho_arquivo, imagem_bytes
            )  # VARIAVEL DE AMBIENTE

            # Gera url pública para a imagem
            url_imagem = f"{SUPABASE_URL}/storage/v1/object/public/post-files/post-files/{unique_filename}"  # VARIAVEL DE AMBIENTE
        return url_imagem

    def save(self, user_id):
        url_imagem = self.get_url_imagem()
        postagem = Postagem(
            titulo=self.titulo.data,
            imagem=url_imagem,  # Se for None, js usará imagem template para o frontend
            conteudo=self.conteudo.data,
            user_id=user_id,
        )

        db.session.add(postagem)
        db.session.commit()

    def update(self, post):
        post.titulo = self.titulo.data
        post.conteudo = self.conteudo.data

        if self.imagem.data and self.imagem.data.filename:
            if post.imagem:
                try:
                    supabase.storage.from_("post-files").remove(
                        ["post-files/" + post.imagem.split("/")[-1]]
                    )  # VARIAVEL DE AMBIENTE
                except SupabaseManagementFileError as e:
                    flash(f"Erro ao excluir arquivo de imagem no Supabase: {e}")

            url_imagem = self.get_url_imagem()
            post.imagem = url_imagem

        if request.form.get("removerImagemPost"):
            if post.imagem:
                supabase.storage.from_("post-files").remove(
                    ["post-files/" + post.imagem.split("/")[-1]]
                )  # VARIAVEL DE AMBIENTE
            post.imagem = None

    def delete(self, post):
        if post.imagem:
            try:
                supabase.storage.from_("post-files").remove(
                    ["post-files/" + post.imagem.split("/")[-1]]
                )  # VARIAVEL DE AMBIENTE
            except SupabaseManagementFileError as e:
                flash(f"Erro ao excluir arquivo de imagem no Supabase: {e}")

        try:
            db.session.delete(post)
            db.session.commit()
            return jsonify({"success": True}), 200
        except QueryObjectManagementError as e:
            db.session.rollback()
            return jsonify({"success": False, "error": str(e)}), 500


class MateriaisForm(FlaskForm):
    destino = SelectField(
        "Destino",
        choices=[(1, "1º Ano"), (2, "2º ano"), (3, "3º ano"), (4, "Olímpiadas")],
        validators=[DataRequired()],
    )
    titulo = StringField("Título", validators=[DataRequired()])
    aula = StringField("Link da aula")
    resumo = FileField("Resumo")
    lista_exercicios = FileField("Lista de Exercícios")
    btnSubmit = SubmitField("Enviar")

    @staticmethod
    def generate_unique_filename(filename):
        return f"{int(time.time())}_{secure_filename(filename)}"

    def upload_para_supabase(self, arquivo):
        """Faz upload de um arquivo para o Supabase Storage e retorna a URL."""

        if arquivo and arquivo.filename:
            unique_filename = self.generate_unique_filename(arquivo.filename)
            file_path = f"/{unique_filename}"
            file_bytes = arquivo.read()

            supabase.storage.from_("material-files").upload(
                file_path, file_bytes, file_options={"content-type": arquivo.mimetype}
            )

            return f"{SUPABASE_URL}/storage/v1/object/public/material-files/{unique_filename}"

        return None

    def verificarMaterial(self):
        """Verifica se pelo menos um material foi enviado"""
        return any(
            [
                self.aula.data.strip(),
                self.resumo.data and self.resumo.data.filename,
                self.lista_exercicios.data and self.lista_exercicios.data.filename,
            ]
        )

    def save(self):
        if self.verificarMaterial():
            resumo_url = self.upload_para_supabase(self.resumo.data)
            lista_exercicios_url = self.upload_para_supabase(self.lista_exercicios.data)

            material = Material(
                destino=self.destino.data,
                titulo=self.titulo.data,
                aula=self.aula.data.strip() or None,
                resumo=resumo_url,
                lista_exercicios=lista_exercicios_url,
            )

            db.session.add(material)
            db.session.commit()
        else:
            raise ResourceNotSentError("Nenhum material enviado...")

    def update(self, material):

        material.destino = self.destino.data
        material.titulo = self.titulo.data
        material.aula = self.aula.data.strip() or None

        if request.form.get("removerMapaMental"):
            if material.resumo:
                supabase.storage.from_("material-files").remove(
                    [material.resumo.split("/")[-1]]
                )  # VARIAVEL DE AMBIENTE
            material.resumo = None

        if request.form.get("removerListaExercicios"):
            if material.lista_exercicios:
                supabase.storage.from_("material-files").remove(
                    [material.lista_exercicios.split("/")[-1]]
                )
            material.lista_exercicios = None

        if self.resumo.data and self.resumo.data.filename:
            if material.resumo:
                try:
                    supabase.storage.from_("material-files").remove(
                        [material.resumo.split("/")[-1]]
                    )
                except SupabaseManagementFileError as e:
                    flash(f"Erro ao excluir o arquivo mapa mental no Supabase: {e}")

            resumo_url = self.upload_para_supabase(self.resumo.data)
            material.resumo = resumo_url
        if self.lista_exercicios.data and self.lista_exercicios.data.filename:
            if material.lista_exercicios:
                try:
                    supabase.storage.from_("material-files").remove(
                        [material.lista_exercicios.split("/")[-1]]
                    )
                except SupabaseManagementFileError as e:
                    flash(
                        f"Erro ao excluir o arquivo lista de exercícios no Supabase: {e}"
                    )

            lista_exercicios_url = self.upload_para_supabase(self.lista_exercicios.data)
            material.lista_exercicios = lista_exercicios_url

    def delete(self, material):
        if material.resumo:
            try:
                supabase.storage.from_("material-files").remove(
                    [material.resumo.split("/")[-1]]
                )
            except SupabaseManagementFileError as e:
                flash(f"Erro ao deletar resumo: {e}")

        if material.lista_exercicios:
            try:
                supabase.storage.from_("material-files").remove(
                    [material.lista_exercicios.split("/")[-1]]
                )
            except SupabaseManagementFileError as e:
                flash(f"Erro ao deletar lista de exercícios: {e}")

        try:
            db.session.delete(material)
            db.session.commit()
            return jsonify({"success": True})
        except QueryObjectManagementError as e:
            db.session.rollback()
            return jsonify({"success": False, "error": str(e)}), 500


# DEPRECATED AREA


# Cadastro de usuário desativado por ser desnecessário após o cadastro do cliente principal
# Cadastro de usuario
class UserForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    sobrenome = StringField("Sobrenome", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    confirmacao_senha = PasswordField(
        "Confirmar senha", validators=[DataRequired(), EqualTo("senha")]
    )
    btnSubmit = SubmitField("Cadastrar")

    # def com validate propria para verificar se email e unico.
    def validate_email(self, email):
        """Verifica se o email já existe e, em caso afirmativo, levanta ValidationError.
        Funções validate_<nome_do_campo>(self, field) são invocados automaticamente pelo WTForms.
        """
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Usuário já cadastrado com este E-mail.")

    # Cadastro no banco de dados
    def save(self):
        # gera hash para senha criptografada que permite caracteres especiais.

        senha = bcrypt.generate_password_hash(self.senha.data).decode("utf-8")
        if not str(senha).startswith(
            "$2b$"
        ):  # Verifica se o hash não está no formato bcrypt
            raise EncryptationFailureError(
                "Houve um erro ao salvar sua senha. Tente novamente ou entre em contato."
            )

        user = User(
            nome=self.nome.data,
            sobrenome=self.sobrenome.data,
            email=self.email.data,
            senha=senha,
        )

        # salva o usuario na sessão e passa para o banco de dados
        db.session.add(user)
        db.session.commit()
        return user
