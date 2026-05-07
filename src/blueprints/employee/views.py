from flask_login import login_required
from flask import Blueprint, render_template
from src.decorator import role_required

employee_bp = Blueprint('employee', __name__)

@employee_bp.route("/dashboard")
@login_required
@role_required('Segurança')
def dashboard():
    return render_template("dashboards/security_dashboard.html")
