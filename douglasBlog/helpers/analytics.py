import uuid
import time

from flask import request, make_response

from douglasBlog import db
from douglasBlog.models_analytics import PageView


# ------------------------------------------
# Geração e leitura do visitor_id (UUID)
# ------------------------------------------


def get_visitor_id():
    """
    Tenta ler o cookie 'visitor_id'.
    Retorna a string do UUID, ou None se não existir.
    """

    return request.cookies.get("visitor_id")


def generate_visitor_id():
    """
    Gera um novo UUID4.
    UUID v4 é aleatório, garantindo unicidade global
    sem expor dados do usuário.
    """

    return str(uuid.uuid4())


# ------------------------------------------
# Controle de Frequência (Dedupe)
# ------------------------------------------

# Nota: este cache é apenas exemplo em memória.
# TODO: Em produção, use Redis ou similar para compartilhar entre processos.
_last_view_times = {}


def is_allowed_to_track(visitor_id: str, path: str, cooldown: int = 300) -> bool:
    """
    Verifica se devemos contar uma nova view para este visitor_id + path
    dentro do período de cooldown.
    Armazena a última timestamp permitida em _last_view_times.
    """

    key = f"{visitor_id}:{path}"
    now = time.time()
    last = _last_view_times.get(key, 0)

    if now - last > cooldown:
        _last_view_times[key] = now
        # print("oi")
        return True
    # print("cooldown")
    return False


# ------------------------------------------
# Inserção do registro no Banco de Dados
# ------------------------------------------


def record_page_view(visitor_id: str, path: str) -> None:
    """
    Insere registro em PageView.
    Faz commit de um único objeto,
    isolando a responsabilidade dessa função.
    """

    pv = PageView(visitor_id=visitor_id, path=path)
    db.session.add(pv)
    db.session.commit()


# ------------------------------------------
# Decorator para trackeamento de views
# ------------------------------------------


def track_page_view(func):

    def wrapper(*args, **kwargs):

        # Transforma View em Response para .set_cookie.
        resp = make_response(func(*args, **kwargs))

        # 1º Tenta ler o cookie 'visitor_id' ou gera um novo
        visitor_id = get_visitor_id()
        new_cookie = False

        if not visitor_id:
            visitor_id = generate_visitor_id()
            new_cookie = True

            # print("1º etapa")

        # 2º Dedupe e Gravação
        path = request.path
        if is_allowed_to_track(visitor_id, path):
            record_page_view(visitor_id, path)

            # print("2º etapa")

        # #3º Se for novo visitor, marca Cookie no cliente
        if new_cookie:
            # Cookie com duração de 1 ano
            resp.set_cookie(
                "visitor_id",
                visitor_id,
                max_age=365 * 24 * 3600,
                httponly=True,
                samesite="Lax",
            )
            # print("3º etapa")

        return resp

    # Preserva metadados da função original
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__

    # print("gravado.")
    return wrapper
