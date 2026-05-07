from flask_login import login_required
from flask import Blueprint, render_template
from src.decorator import role_required

supervisor_bp = Blueprint('security', __name__)

@supervisor_bp.route("/dashboard")
@login_required
@role_required('Supervisor')
def dashboard():
    return render_template("dashboards/supervisor_dashboard.html")