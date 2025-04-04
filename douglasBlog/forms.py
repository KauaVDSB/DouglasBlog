from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField, FileField
# Para validar email, baixar biblioteca email_validator
from wtforms.validators import DataRequired, Email#, EqualTo, ValidationError

# from flask_login import current_user

from douglasBlog import app, db, bcrypt, supabase, SUPABASE_URL
from douglasBlog.models import User, Postagem, Material

import time
from werkzeug.utils import secure_filename




class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Entrar')

    def login(self):
        # Procura pelo usuário afim de resgatar os dados.
        user = User.query.filter_by(email=self.email.data).first()

        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data.encode('utf-8')):
                print("Usuário logado com sucesso!")
                return user
            else:
                raise Exception('Senha incorreta.')
        else:
            raise Exception('Usuário não encontrado.')


class PostagemForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    imagem = FileField('Imagem')
    conteudo = TextAreaField('Conteúdo')
    btnSubmit = SubmitField('Publicar')

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
            supabase.storage.from_("post-files").upload(caminho_arquivo, imagem_bytes)

            # Gera url pública para a imagem
            url_imagem = f"{SUPABASE_URL}/storage/v1/object/public/post-files/post-files/{unique_filename}"
        return url_imagem


    def save(self, user_id):
        url_imagem = self.get_url_imagem()
        postagem = Postagem(
            titulo = self.titulo.data,
            imagem = url_imagem, # Se for None, js usará imagem template para o frontend
            conteudo = self.conteudo.data,
            user_id = user_id
        )

        db.session.add(postagem)
        db.session.commit()


class MateriaisForm(FlaskForm):
    destino = SelectField(u'Destino', choices=[
        (1, '1º Ano'), (2, '2º ano'), (3, '3º ano'), (4, 'Olímpiadas')
        ], validators=[DataRequired()])
    titulo = StringField('Título', validators=[DataRequired()])
    aula = StringField('Link da aula')
    mapa_mental = FileField('Mapa Mental')
    lista_exercicios = FileField('Lista de Exercícios')
    btnSubmit = SubmitField('Enviar')


    @staticmethod
    def generate_unique_filename(filename):
        return f"{int(time.time())}_{secure_filename(filename)}"

    def upload_para_supabase(self, arquivo):
        """Faz upload de um arquivo para o Supabase Storage e retorna a URL."""

        if arquivo and arquivo.filename:
            unique_filename = self.generate_unique_filename(arquivo.filename)
            file_path = f"/{unique_filename}"
            file_bytes = arquivo.read()

            supabase.storage.from_('material-files').upload(
                file_path,
                file_bytes,
                file_options={"content-type":arquivo.mimetype}
            )

            return f"{SUPABASE_URL}/storage/v1/object/public/material-files/{unique_filename}"

        return None


    def verificarMaterial(self):
        """Verifica se pelo menos um material foi enviado"""
        return any([
            self.aula.data.strip(),
            self.mapa_mental.data and self.mapa_mental.data.filename,
            self.lista_exercicios.data and self.lista_exercicios.data.filename
        ])


    def save(self):
        if self.verificarMaterial():
            mapa_mental_url = self.upload_para_supabase(self.mapa_mental.data)
            lista_exercicios_url = self.upload_para_supabase(self.lista_exercicios.data)
            
            material = Material(
                destino=self.destino.data,
                titulo=self.titulo.data,
                aula=self.aula.data.strip() or None,
                mapa_mental=mapa_mental_url,
                lista_exercicios=lista_exercicios_url
            )

            db.session.add(material)
            db.session.commit()
        else:
            raise Exception('Nenhum material enviado...')





# DEPRECATED AREA

# Cadastro de usuário desativado por ser desnecessário após o cadastro do cliente principal
# Cadastro de usuario
#class UserForm(FlaskForm):
#    nome = StringField('Nome', validators=[DataRequired()])
#    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
#    email = StringField('E-mail', validators=[DataRequired(), Email()])
#    senha = PasswordField('Senha', validators=[DataRequired()])
#    confirmacao_senha = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('senha')])
#    btnSubmit = SubmitField('Cadastrar')
#
#    # def com validate propria para verificar se email e unico. 
#    def validade_email(self, email): # Ao dar submit, ele procura todas as def que comecam com 'validade_'.
#        if User.query.filter(email=email.data).first():
#            return ValidationError('Usuário já cadastrado com este E-mail.')
#
#
#    # Cadastro no banco de dados
#    def save(self):
#        # gera hash para senha criptografada que permite caracteres especiais.
#        #senha =  bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))
#        senha = bcrypt.generate_password_hash(self.senha.data).decode('utf-8')
#        if not str(senha).startswith('$2b$'):  # Verifica se o hash não está no formato bcrypt
#            raise Exception('Houve um erro ao salvar sua senha. Tente novamente ou entre em contato.')
#
#
#        user = User(
#            nome = self.nome.data,
#            sobrenome = self.sobrenome.data,
#            email = self.email.data,
#            senha = senha
#        )
#
#        # salva o usuario na sessão e passa para o banco de dados
#        db.session.add(user)
#        db.session.commit()
#        return user
