from extensions import db
from sqlalchemy import Enum
from datetime import date

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    #username = db.Column(db.String(30), nullable = False, unique = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    #cpf = db.Column(db.String(11), nullable = False, unique = True)
    #dt_nasc = db.Column(db.Date, nullable = False)
    password = db.Column(db.String(255), nullable = False)

class Task(db.Model):
    __tablename__ = "tasks"
    __table_args__ = (db.UniqueConstraint("id_user", "title", name="unique_user_title"),)

    id = db.Column(db.Integer, primary_key = True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(300), nullable = False)
    prazo = db.Column(db.Date, nullable = False)
    status = db.Column(Enum("pendente", "concluido", name = "status_task"), nullable = False)

    user = db.relationship("User", backref = db.backref('tasks', lazy = True, cascade = "all, delete-orphan"))

    @property
    def fora_do_prazo(self):
        return self.status == "pendente" and self.prazo < date.today()
    
    