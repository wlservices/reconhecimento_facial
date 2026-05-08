from flask_login import login_required
from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.decorator import role_required
from src.models.user import User
from src.extensions import db
from datetime import datetime


supervisor_bp = Blueprint('supervisor', __name__)

@supervisor_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
@role_required('Supervisor')
def dashboard():
    lista_usuarios = User.query.filter(User.role == 'Funcionario').all()

    now = datetime.now()

    form_type = request.form.get('form_action')

    if form_type == 'create_user':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        if username and password:
            novo_usuario = User(username=username, role=role)
            novo_usuario.set_password(password)
            db.session.add(novo_usuario)
            db.session.commit()
            flash("Usuário criado!")

        return redirect(url_for('supervisor.dashboard'))

    return render_template("dashboards/supervisor_dashboard.html", usuarios=lista_usuarios, data_atual=now)