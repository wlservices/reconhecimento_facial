from flask import Flask
from src.routes.view import views_bp
from src.extensions import db
from flask_login import LoginManager
from flask_migrate import Migrate
from src.models.user import User
from src.blueprints.admin.views import admin_bp
from src.blueprints.supervisor.views import supervisor_bp
from src.blueprints.employee.views import employee_bp
import os


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_ADDRESS = os.getenv("DB_ADDRESS")
DB_NAME = os.getenv("DB_NAME")


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder="src/templates",
    static_folder="src/static",
)

# Configuração do banco (SQLite por padrão)
"""
Quando quiser migrar para PostgresQL so usar esse trecho no lugar do outro!:
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://DB_USER:DB_PASSWORD@DB_ADDRESS/DB_NAME"
"""
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'src', 'data', 'database.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY_FLASK")

db.init_app(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "view.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(views_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(supervisor_bp, url_prefix='/supervisor')
app.register_blueprint(employee_bp, url_prefix='/employee')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
