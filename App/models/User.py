from datetime import datetime

from App import db


class Usuario(db.Model):
    __tablename__ = 'user_app'
    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(260), nullable=False)
    password = db.Column(db.Text, nullable=False)
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id_rol'))
    foto_perfil = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=datetime.now)
    is_Active = db.Column(db.Integer, nullable=False, default=1)
    update_on = db.Column(db.DateTime, default=None)

    def __init__(self, email, password, id_role, foto_perfil):
        self.email = email
        self.password = password
        self.id_rol = id_role
        self.foto_perfil = foto_perfil

    def __repr__(self):
        return f'<email:{self.Email}>'


class Roles(db.Model):
    __tablename__ = 'roles'
    id_rol = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_rol = db.Column(db.String(150))
    created_on = db.Column(db.DateTime, default=datetime.now)
    is_Active = db.Column(db.Integer, nullable=False, default=1)
    update_on = db.Column(db.DateTime, default=None)

    def __init__(self, nombre_rol):
        self.nombre_rol = nombre_rol

    def __repr__(self):
        return f'<nombre_rol:{self.nombre_rol}>'
