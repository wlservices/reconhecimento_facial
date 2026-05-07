from flask_login import login_required
from flask import Blueprint, render_template
from src.decorator import role_required
from src.models.user import User
from datetime import datetime


admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard")
@login_required
@role_required('Administrador')
def dashboard():
    usuarios = User.query.all()
    now = datetime.now()
    return render_template("dashboards/admin_dashboard.html", lista_usuarios=usuarios, data_atual=now)