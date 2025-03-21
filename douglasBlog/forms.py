from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField

# Para validar email, baixar biblioteca email_validator
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from flask_login import current_user

from douglasBlog import db, bcrypt
from douglasBlog.models import User


# Cadastro de usuario
class UserForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('senha')])
    btnSubmit = SubmitField('Cadastrar')

    # def com validate propria para verificar se email e unico. 
    def validade_email(self, email): # Ao dar submit, ele procura todas as def que comecam com 'validade_'.
        if User.query.filter(email=email.data).first():
            return ValidationError('Usuário já cadastrado com este E-mail.')


    # Cadastro no banco de dados
    def save(self):
        # gera hash para senha criptografada que permite caracteres especiais.
        #senha =  bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))
        senha = bcrypt.generate_password_hash(self.senha.data).decode('utf-8')
        if not str(senha).startswith('$2b$'):  # Verifica se o hash não está no formato bcrypt
            raise Exception('Houve um erro ao salvar sua senha. Tente novamente ou entre em contato.')


        user = User(
            nome = self.nome.data,
            sobrenome = self.sobrenome.data,
            email = self.email.data,
            senha = senha
        )

        # salva o usuario na sessão e passa para o banco de dados
        db.session.add(user)
        db.session.commit()
        return user

