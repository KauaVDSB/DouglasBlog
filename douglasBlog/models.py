# pylint: disable=too-few-public-methods

import re

from datetime import datetime
from flask_login import UserMixin

from douglasBlog import db, login_manager


@login_manager.user_loader  # Retorna sessao do usuario no controle de login
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=True)
    sobrenome = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    senha = db.Column(db.String, nullable=True)

    data_cadastro = db.Column(db.DateTime, default=datetime.now())
    admin = db.Column(db.Boolean, default=False)
    # É referenciado pela tabela Postagem para salvar autoria nas postagens
    postagem = db.relationship("Postagem", backref="user", lazy=True)


class Postagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=True)
    imagem = db.Column(db.String)
    conteudo = db.Column(db.Text, nullable=True)
    data_postagem = db.Column(db.DateTime, default=datetime.now())
    # Referencia a tabela User para obter informacoes
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    def conteudoResumo(self):
        len_conteudo = len(self.conteudo)
        post_conteudo = re.sub(r"<[^>]*?>", "", self.conteudo)  # Remove tags HTML
        if len_conteudo > 60:
            return f"{post_conteudo[:37]}..."
        return post_conteudo

    def data_resumo(self):
        data = str(self.data_postagem)[:16].replace(":", "h")
        data = data.replace("-", "/")
        dataOrdem = data[8:10] + "/" + data[5:8] + data[:4] + data[10:]
        return dataOrdem


class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destino = db.Column(db.Integer, nullable=False)
    titulo = db.Column(db.String, nullable=False)
    aula = db.Column(db.Text, nullable=True)
    resumo = db.Column(db.Text, nullable=True)
    atividade = db.Column(db.Text, nullable=True)
    lista_exercicios = db.Column(db.Text, nullable=True)
    gabarito = db.Column(db.Text, nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.now())

    def data_resumo(self):
        data = str(self.data_criacao)[:16].replace(":", "h")
        data = data.replace("-", "/")
        dataOrdem = data[8:10] + "/" + data[5:8] + data[:4] + data[10:]
        return dataOrdem
