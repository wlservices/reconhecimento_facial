from flask_login import login_required
from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.decorator import role_required
from src.models.user import User
from datetime import datetime
from  src.extensions import db


admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
@role_required('Administrador')
def dashboard():
    lista_usuarios = User.query.all()
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

        return redirect(url_for('admin.dashboard'))

    return render_template("dashboards/admin_dashboard.html", usuarios=lista_usuarios, data_atual=now)

@admin_bp.route('/get-modal-usuario') #
@login_required #
def get_modal(): #
    return render_template('includes/_create_users.html') #
