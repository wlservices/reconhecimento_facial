from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from src.extensions import db


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    photo = db.Column(db.String(200), nullable=True)

    def get_username(self):
        return self.username
    
    def get_role(self):
        return self.role
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def set_role(self, new_role):
        self.role = new_role

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"<User {self.username} - {self.get_role}>"

    def __str__(self):
        return f"Usuario: {self.username} / Cargo: {self.role}"
    