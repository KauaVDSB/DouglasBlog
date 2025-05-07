# pylint: disable=cyclic-import

from flask import jsonify, request
from flask_login import login_required

from douglasBlog import app
from douglasBlog.helpers.analytics import get_total_views, get_views_by_period
from douglasBlog.helpers.permission import VerificarAdmin
from douglasBlog.exceptions import GetAPIError


@app.route("/api/analytics/total")
def api_total_views():
    """
    Rota de livre acesso, para consumo na navbar.
    """
    total = get_total_views()
    return jsonify(total=total)


@app.route("/api/analytics/<period>")
@login_required
def api_views_by_period(period):
    VerificarAdmin()
    path = request.args.get("path")
    try:
        data = get_views_by_period(period, path=path)
    except GetAPIError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(data)
