from src.models.user import User
from flask import Blueprint, render_template, url_for, redirect, request, flash, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from src.extensions import db
import os
import base64


views_bp = Blueprint("view", __name__)

@views_bp.after_request
def add_header(response):
    # Impede o cache de páginas protegidas
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@views_bp.route("/", methods=["GET", "POST"])
def login():

    admin_exists = User.query.filter_by(role="Administrador").first()

    if not admin_exists:
        return redirect(url_for("view.first_access"))
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Busca usuario no banco
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            if user.role == 'Administrador':
                return redirect(url_for("admin.dashboard"))
            elif user.role == 'Supervisor':
                return redirect(url_for("supervisor.dashboard"))
            else:
                return redirect(url_for("employee.dashboard"))
        else:
            flash('Usuario ou Senha invalido')
            return redirect(url_for("view.login") + "#meu-modal")
        
    return render_template("login.html")


@views_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("view.login"))


@views_bp.route("/first_access", methods=["GET", "POST"])
def first_access():

    # Verifica se já existe um admin
    admin_exists = User.query.filter_by(role="Administrador").first()

    if admin_exists:
        # Se já existe, redireciona para login normal
        return redirect(url_for("view.login"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Cria o admin
        admin = User(username=username, role="Administrador")
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()

        flash("Administrador criado com sucesso!", "sucess")

        # Faz login automático
        login_user(admin)
        return redirect(url_for("view.homepage"))

    return render_template("first_access.html")


@views_bp.route("/update-profile", methods=["GET", "POST"])
@login_required
def update_profile():
    if request.method == "POST":
        name = request.form.get('name')
        role = request.form.get('role')
        cropped_data = request.form.get('cropped_image') # String Base64 do Cropper

        # 1. Prioridade para a imagem recortada (Cropper)
        if cropped_data and "," in cropped_data:
            header, encoded = cropped_data.split(",", 1)
            data = base64.b64decode(encoded)

            # Use () se getId for um método, ou tire se for atributo. 
            # Geralmente no Flask-Login é current_user.id
            filename = f"user_{current_user.id}.jpg"
            
            # Pasta de destino
            upload_dir = os.path.join(current_app.static_folder, "uploads")
            os.makedirs(upload_dir, exist_ok=True) # Garante que a pasta existe
            
            file_path = os.path.join(upload_dir, filename)

            with open(file_path, "wb") as f:
                f.write(data) # Corrigido: era f.write, não f.f.write

            current_user.photo = f"uploads/{filename}"

        # 2. Se não veio recorte, mas veio arquivo direto (fallback)
        elif 'photo' in request.files:
            file = request.files.get('photo')
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.static_folder, "uploads", filename))
                current_user.photo = f"uploads/{filename}"

        # 3. Atualiza os textos
        current_user.username = name
        current_user.role = role

        db.session.commit()

        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for("view.homepage"))
    
    return render_template("profile_settings.html")
