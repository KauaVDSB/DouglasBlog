from douglasBlog import db, login_manager
from datetime import datetime
from flask_login import UserMixin, login_user, logout_user, current_user 



@login_manager.user_loader # Retorna sessao do usuario no controle de login
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Boolean, default=False)
    nome = db.Column(db.String, nullable=True)
    sobrenome = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    senha = db.Column(db.String, nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.now())
    