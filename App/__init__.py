import pyodbc
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash

from App.controllers.HomeController import home_bp
from App.controllers.AuthController import auth_bp
from App.controllers.registrarController import registrar_bp
from App.controllers.InformacionController import informacion_bp

from config import Config

jwt = JWTManager()
db = SQLAlchemy()


def crear_base_datos(nombre_bd):
    try:
        driver = 'ODBC Driver 17 for SQL Server'

        conn_str = (f'DRIVER={{{driver}}};SERVER={Config.DB_SERVER};UID={Config.DB_USER};PWD={Config.DB_PASSWORD};'
                    f'TrustServerCertificate=yes')

        # Conectar al servidor
        conn = pyodbc.connect(conn_str, autocommit=True)
        cursor = conn.cursor()

        # Verificar si la base de datos ya existe
        cursor.execute("SELECT name FROM sys.databases")
        bases_de_datos = [row.name for row in cursor.fetchall()]

        if nombre_bd in bases_de_datos:
            print(f"La base de datos '{nombre_bd}' ya existe.")
        else:
            # Crear la base de datos si no existe
            cursor.execute(f"CREATE DATABASE {nombre_bd}")

        # Cerrar la conexión
        cursor.close()
        conn.close()

    except pyodbc.Error as e:
        print(f"Error al verificar/crear la base de datos: {e}")


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    crear_base_datos("Sistema_votacion")  # Crear la base de datos si no existe

    db.init_app(app)

    jwt.init_app(app)

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(registrar_bp)
    app.register_blueprint(informacion_bp)

    from App.models.sistemaModel import (Lider, LiderRespBarrios,
                                         Barrio, Comuna, CapitanComuna, Capitan, Municipio, DatosVotante,
                                         PuestoVotacion, datetime)
    from App.models.User import Roles, Usuario

    with app.app_context():
        db.create_all()
        # Verificar si el rol de administrador existe
        admin_role = Roles.query.filter_by(nombre_rol='Administrador').first()
        if not admin_role:
            admin_role = Roles(nombre_rol='Administrador')
            db.session.add(admin_role)
            db.session.commit()

        lider_role = Roles.query.filter_by(nombre_rol='Lider').first()
        if not lider_role:
            lider_role = Roles(nombre_rol='Lider')
            db.session.add(lider_role)
            db.session.commit()
        # Verificar si el usuario administrador existe
        admin_user = Usuario.query.filter_by(email='admin@example.com').first()
        if not admin_user:
            password = generate_password_hash("admin123")
            admin_user = Usuario(email='admin@example.com', password=password, id_role=admin_role.id_rol,
                                 foto_perfil='images/messages-3.jpg')
            db.session.add(admin_user)
            db.session.commit()
            id = admin_user.id_user
            
            lider_add = Lider(nombres='admin', apellidos='admin', celular='0', capitan_id=None,
                              id_rol=admin_role.id_rol, id_user_app=id, direccion='admin'
                              , pais=None, nacimiento=None, ciudad=None)

            db.session.add(lider_add)
            db.session.commit()

    return app
