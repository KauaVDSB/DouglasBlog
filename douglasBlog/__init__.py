import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from supabase import create_client


load_dotenv(".env")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config["UPLOAD_FILES"] = r"static/data"

# Configurar as credenciais do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = (
    "homepage"  # Se usuario nao estiver logado, sera redirecionado para esta view
)
bcrypt = Bcrypt(app)


# Variáveis de ambiente

ACESSO_CADASTRO = os.getenv("ACESSO_CADASTRO")
ACESSO_LOGIN = os.getenv("ACESSO_LOGIN", "login_default")


@app.context_processor
def inject_environment_variables():
    return {"ACESSO_LOGIN": ACESSO_LOGIN}


from douglasBlog.routes import (  # noqa: F401,E402  # pylint: disable=unused-import,wrong-import-position
    homepage,
)

from douglasBlog.models_analytics import (  # noqa: F401,E402  # pylint: disable=unused-import,wrong-import-position
    PageView,
)
