import os
from dotenv import load_dotenv

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from supabase import create_client

# Outras extensões
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
supabase_client = None
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

ACESSO_CADASTRO = os.getenv("ACESSO_CADASTRO")
ACESSO_LOGIN = os.getenv("ACESSO_LOGIN", "login_default")


def create_app():
    # Carrega variáveis de ambiente
    load_dotenv(".env")

    app = Flask(__name__, static_folder="static", template_folder="templates")

    # Configurações
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY=os.getenv("SECRET_KEY"),
        UPLOAD_FILES=os.path.join(
            app.root_path, "static", "data"
        ),  # Para upload interno, utilizado em breve.
    )

    # Inicialização das extensões
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "base.homepage"

    @login_manager.unauthorized_handler
    def handle_needs_login():
        return redirect(url_for("base.homepage"))

    bcrypt.init_app(app)

    # Configurar Supabase
    global supabase_client
    supabase_client = create_client(
        SUPABASE_URL, SUPABASE_KEY
    )

    # Registro de Blueprints
    from douglasBlog.base.routes import base_bp
    from douglasBlog.auth.routes import auth_bp
    from douglasBlog.blog.routes import blog_bp
    from douglasBlog.materials.routes import materials_bp
    from douglasBlog.admin.routes import admin_bp

    app.register_blueprint(base_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(blog_bp, url_prefix="/blog")
    app.register_blueprint(materials_bp, url_prefix="/materials")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Injeção de variáveis para templates
    @app.context_processor
    def inject_env():
        return {
            "ACESSO_CADASTRO": os.getenv("ACESSO_CADASTRO"),
            "ACESSO_LOGIN": os.getenv("ACESSO_LOGIN", "login_default"),
        }

    return app


# Para WSGI
app = create_app()
from douglasBlog.base.routes import homepage