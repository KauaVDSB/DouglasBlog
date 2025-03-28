from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField, FileField
# Para validar email, baixar biblioteca email_validator
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from flask_login import current_user

from douglasBlog import app, db, bcrypt
from douglasBlog.models import User, Postagem, Material

import os
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

    def save(self, user_id):
        imagem = self.imagem.data
        print(imagem)
        nome_seguro = secure_filename(imagem.filename)
        postagem = Postagem(
            titulo = self.titulo.data,
            imagem = nome_seguro,
            conteudo = self.conteudo.data,
            user_id = user_id
        )

        caminho = os.path.join(
            # Pasta do projeto
            os.path.abspath(os.path.dirname(__file__)),
            # Pasta de UPLOAD
            app.config['UPLOAD_FILES'],
            # Pasta do post
            'post',
            # Arquivo
            nome_seguro
        )

        imagem.save(caminho)
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


    def caminhoArquivo(self, arquivo):
        arquivo_recebido = arquivo
        print(arquivo_recebido)
        nome_seguro = secure_filename(arquivo_recebido.filename)

        caminho = os.path.join(
            # Pasta do projeto
            os.path.abspath(os.path.dirname(__file__)),
            # Pasta de UPLOAD
            app.config['UPLOAD_FILES'],
            # Pasta do material
            'material',
            # Arquivo
            nome_seguro
        )

        arquivo_recebido.save(caminho)
        return nome_seguro

    def verificarMaterial(self):
        lista_conteudos = [self.aula.data, self.mapa_mental.data, self.lista_exercicios.data]
        tem_material = []
        materiais = ""
        for conteudo in range(len(lista_conteudos)):
            if lista_conteudos[conteudo] != "":
                tem_material = tem_material + [conteudo]
            

        if (len(tem_material) > 0):
            hash = " KEWFNIUHWKN3IN3JHR32KJRB3298HF33MRN32KB32KUB32IB3IBFERFKEWFNIUHWKN3IN3JHR32KJRB3298HF33MRN32KB32KUB32IB3IBFERF "
            for conteudo in range(len(tem_material)):
                if tem_material[conteudo] == 0:
                    materiais = materiais + "<div class='container-aula'>" + self.aula.data + hash
                elif tem_material[conteudo] == 1:
                    materiais = materiais + "<div class='container-mapa-mental'>" + self.caminhoArquivo(self.mapa_mental.data) + hash
                else:
                    materiais = materiais + "<div class='container-lista-exercicios'>" + self.caminhoArquivo(self.lista_exercicios.data)
            return materiais
        else:
            raise Exception('Nenhum material enviado...')


    def save(self):
        materiais = self.verificarMaterial()
        if materiais != '':
            material = Material(
                destino = self.destino.data,
                titulo = self.titulo.data,
                materiais = materiais
            )

            db.session.add(material)
            db.session.commit()





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
