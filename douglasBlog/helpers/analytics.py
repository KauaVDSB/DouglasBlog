import uuid
import time
from typing import Optional, List, Dict, Any

from flask import request, make_response
from sqlalchemy import func, text
from douglasBlog import db
from douglasBlog.models_analytics import PageView


# Nota: este cache é apenas exemplo em memória.
# Em produção, use Redis ou similar para compartilhar entre processos.
_last_view_times = {}


# ------------------------------------------
# Funções de Query para Analytics
# ------------------------------------------


def get_total_views() -> int:
    return db.session.query(func.count(PageView.id)).scalar()


def get_views_by_period(
    period: str, path: Optional[str] = None
) -> List[Dict[str, Any]]:
    # path: str | None = None funciona apenas a partir de Python3.10
    """
    period: 'daily', 'weekly', 'monthly'
    path: rota específica ou None (opcional)

    Retorna lista de { period: ISODate, views: int }.
    """

    mapping = {
        "daily": ("30 days", "day"),
        "weekly": ("12 weeks", "week"),
        "monthly": ("12 months", "month"),
    }

    if period not in mapping:
        raise ValueError(f"Período inválido: {period}")

    interval, trunc = mapping[period]

    q = (
        db.session.query()
        .with_entities(
            func.date_trunc(trunc, PageView.occurred_at).label("period"),
            func.count(PageView.id).label("views"),
        )
        .filter(PageView.occurred_at > func.now() - text(f"interval '{interval}'"))
    )

    if path:
        q = q.filter(PageView.path == path)

    q = q.group_by("period").order_by("period")

    return [{"period": row.period.isoformat(), "views": row.views} for row in q.all()]


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
    Insere registro em PageView. Faz o import de db e do modelo só aqui,
    quando realmente vamos gravar no banco, para não criar ciclo.
    """
    from douglasBlog import db  # pylint: import-outside-toplevel
    from douglasBlog.models_analytics import PageView  # pylint: import-outside-toplevel

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
