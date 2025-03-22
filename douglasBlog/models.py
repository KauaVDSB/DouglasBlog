from douglasBlog import db, login_manager
from datetime import datetime
from flask_login import UserMixin, login_user, logout_user, current_user 



@login_manager.user_loader # Retorna sessao do usuario no controle de login
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
    postagem = db.relationship('Postagem', backref='user', lazy=True)



class Postagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=True)
    conteudo = db.Column(db.Text, nullable=True)
    data_postagem = db.Column(db.DateTime, default=datetime.now())
    # Referencia a tabela User para obter informacoes
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) 