from datetime import datetime

from App import db


class Municipio(db.Model):
    __tablename__ = 'municipio'
    id_municipio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return f'<Municipio {self.nombre}>'


class Comuna(db.Model):
    __tablename__ = 'comuna'
    id_comuna = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    municipio_id = db.Column(db.Integer, db.ForeignKey('municipio.id_municipio'), nullable=False)

    def __init__(self, nombre, municipio_id):
        self.nombre = nombre
        self.municipio_id = municipio_id

    def __repr__(self):
        return f'<Comuna {self.nombre}>'


class Barrio(db.Model):
    __tablename__ = 'barrio'
    id_barrio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    comuna_id = db.Column(db.Integer, db.ForeignKey('comuna.id_comuna'), nullable=False)

    def __init__(self, nombre, comuna_id):
        self.nombre = nombre
        self.comuna_id = comuna_id

    def __repr__(self):
        return f'<Barrio {self.nombre}>'


class PuestoVotacion(db.Model):
    __tablename__ = 'puesto_votacion'
    id_puesto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    municipio_id = db.Column(db.Integer, db.ForeignKey('municipio.id_municipio'), nullable=False)

    def __init__(self, nombre, direccion, municipio_id):
        self.nombre = nombre
        self.direccion = direccion
        self.municipio_id = municipio_id

    def __repr__(self):
        return f'<PuestoVotacion {self.nombre}>'


class Capitan(db.Model):
    __tablename__ = 'capitan'
    id_capitan = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.String(20), nullable=False)

    def __init__(self, nombres, apellidos, celular):
        self.nombres = nombres
        self.apellidos = apellidos
        self.celular = celular

    def __repr__(self):
        return f'<Capitan {self.nombres} {self.apellidos}>'


class CapitanComuna(db.Model):
    __tablename__ = 'capitan_comuna'
    id_capitancomuna = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comuna_id = db.Column(db.Integer, db.ForeignKey('comuna.id_comuna'))
    capitan_id = db.Column(db.Integer, db.ForeignKey('capitan.id_capitan'))

    def __init__(self, comuna_id, capitan_id):
        self.comuna_id = comuna_id
        self.capitan_id = capitan_id

    def __repr__(self):
        return f'<CapitanComuna {self.comuna_id} {self.capitan_id}>'


class Lider(db.Model):
    __tablename__ = 'lider'
    id_lider = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.String(20), nullable=False)
    direccion = db.Column(db.Text, default=None)
    pais = db.Column(db.String(100), default=None)
    nacimiento = db.Column(db.Date, default=None)
    ciudad = db.Column(db.String(100), default=None)
    capitan_id = db.Column(db.Integer, db.ForeignKey('capitan.id_capitan'))
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id_rol'))
    id_user_app = db.Column(db.Integer, db.ForeignKey('user_app.id_user'))

    def __init__(self, nombres, apellidos, celular, direccion, pais, ciudad, nacimiento, capitan_id, id_rol,
                 id_user_app):
        self.nombres = nombres
        self.apellidos = apellidos
        self.celular = celular
        self.direccion = direccion
        self.pais = pais
        self.ciudad = ciudad
        self.nacimiento = nacimiento
        self.capitan_id = capitan_id
        self.id_rol = id_rol
        self.id_user_app = id_user_app

    def __repr__(self):
        return f'<Lider {self.nombres} {self.apellidos}>'


class LiderRespBarrios(db.Model):
    __tablename__ = 'lider_resp_barrios'
    id_liderresponsable = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lider_id = db.Column(db.Integer, db.ForeignKey('lider.id_lider'), nullable=False)
    capitancomuna_id = db.Column(db.Integer, db.ForeignKey('capitan_comuna.id_capitancomuna'), nullable=False)
    barrio_id = db.Column(db.Integer, db.ForeignKey('barrio.id_barrio'), nullable=False)

    def __init__(self, lider_id, capitancomuna_id, barrio_id):
        self.lider_id = lider_id
        self.capitancomuna_id = capitancomuna_id
        self.barrio_id = barrio_id

    def __repr__(self):
        return f'<LiderRespBarrios {self.lider_id} {self.barrio_id}>'


class DatosVotante(db.Model):
    __tablename__ = 'datos_votante'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    cedula = db.Column(db.String(20), nullable=False)
    lider_id = db.Column(db.Integer, db.ForeignKey('lider.id_lider'), nullable=False)
    barrio_id = db.Column(db.Integer, db.ForeignKey('barrio.id_barrio'), nullable=False)
    puestovotacion_id = db.Column(db.Integer, db.ForeignKey('puesto_votacion.id_puesto'), nullable=False)
    mesa = db.Column(db.String(50), nullable=False)

    def __init__(self, nombres, apellidos, direccion, telefono, cedula, mesa,lider_id,barrio_id,puestovotacion_id):
        self.nombres = nombres
        self.apellidos = apellidos
        self.direccion = direccion
        self.telefono = telefono
        self.cedula = cedula
        self.mesa = mesa
        self.lider_id=lider_id
        self.barrio_id=barrio_id
        self.puestovotacion_id=puestovotacion_id

    def __repr__(self):
        return f'<DatosVotante {self.nombres} {self.apellidos}>'
