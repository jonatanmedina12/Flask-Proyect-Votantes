import os
from datetime import datetime
from flask import Blueprint, render_template, request, url_for, redirect, flash, current_app, session, jsonify
from werkzeug.security import generate_password_hash
from App.controllers.AuthController import login_required
from email_validator import validate_email, EmailNotValidError
import dns.resolver
from App.controllers.geocoding import get_address_details

registrar_bp = Blueprint('registrar', __name__, url_prefix='/registrar')


def is_valid_email_format(email):
    try:
        # Valida el formato y la existencia del correo electrónico
        v = validate_email(email)
        return True
    except EmailNotValidError as e:
        # email no es válido, retorna False
        return False


def is_email_exist(email):
    global domain
    try:
        # Extrae el dominio del correo electrónico
        domain = email.split('@')[1]
        # Resuelve los registros MX para el dominio
        records = dns.resolver.resolve(domain, 'MX')
        return len(records) > 0
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return False
    except dns.exception.DNSException as e:
        # Captura cualquier otro error relacionado con DNS y muestra el mensaje de error
        print(f"Error al resolver el dominio {domain}: {e}")
        return False


@registrar_bp.route('/buscar_direccion')
@login_required
def buscar_direccion():
    direccion = request.args.get('direccion')
    lat, lng, city, department, country = get_address_details(direccion)
    if lat and lng:
        return jsonify({
            'success': True,
            'city': city,
            'department': department,
            'country': country
        })
    else:
        return jsonify({'success': False})


@registrar_bp.route('/registrarVotantes', methods=('GET', 'POST'))
@login_required
def registrarVotantes():
    from App.models.User import Usuario
    from App.models.sistemaModel import Municipio, PuestoVotacion, DatosVotante, Barrio, Lider
    from App import db
    user_foto_perfil = None
    rol = None
    user_id = session.get('user_id')
    if user_id is not None:
        user = Usuario.query.get(user_id)  # Obtener el usuario actual

        user_foto_perfil = user.foto_perfil
        rol = user.id_rol
    municipio_all = Municipio.query.all()
    puesto_votacion_all = PuestoVotacion.query.all()
    barrio_all = Barrio.query.all()
    lider_id = Lider.query.filter_by(id_user_app=user_id).first()

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        cedula = request.form.get('cedula')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')
        barrio = request.form.get('barrio')
        puesto_votacion = request.form.get('puesto_votacion')
        Mesa_votacion = request.form.get('Mesa_votacion')
        cedula_exist = DatosVotante.query.filter_by(cedula=cedula).first()
        if lider_id is None:
            flash('No esta habilitado para registrar votantes valide con el administrador ..')

            return render_template('admin/registrar_Votantes.html', user_foto_perfil=user_foto_perfil, rol=rol
                                   , municipio=municipio_all, puesto=puesto_votacion_all, barrio=barrio_all)

        if cedula_exist is None:
            add = DatosVotante(nombres=nombre, apellidos=apellido, direccion=direccion, telefono=telefono,
                               cedula=cedula, mesa=Mesa_votacion, lider_id=lider_id.id_lider,
                               barrio_id=barrio, puestovotacion_id=puesto_votacion)
            db.session.add(add)
            db.session.commit()  # Commit the session to get the user ID

            return render_template('admin/registrar_Votantes.html', user_foto_perfil=user_foto_perfil, rol=rol
                                   , municipio=municipio_all, puesto=puesto_votacion_all, barrio=barrio_all)
        else:
            flash('Cedula ya registrada')

            return render_template('admin/registrar_Votantes.html', user_foto_perfil=user_foto_perfil, rol=rol
                                   , municipio=municipio_all, puesto=puesto_votacion_all, barrio=barrio_all)

    return render_template('admin/registrar_Votantes.html', user_foto_perfil=user_foto_perfil, rol=rol
                           , municipio=municipio_all, puesto=puesto_votacion_all, barrio=barrio_all)


@registrar_bp.route('/registrar_usuarios', methods=('GET', 'POST'))
@login_required
def registrar_usuarios():
    from App.models.User import Usuario, Roles
    from App.models.sistemaModel import Lider
    from App import db

    roles = Roles.query.all()

    if request.method == 'POST':
        try:
            foto_perfil_path = None
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            celular = request.form['celular']
            direccion = request.form['direccion']
            nacimiento = datetime.strptime(request.form['nacimiento'], '%Y-%m-%d') if request.form[
                'nacimiento'] else None
            role = request.form['role']
            password = request.form['password']
            email = request.form['email']
            # Obtener coordenadas
            latitud, longitud, ciudad, departamento, pais = get_address_details(direccion)

            if not is_valid_email_format(email):
                flash('Formato de correo electrónico no válido')
                return render_template('admin/registrar_users.html', roles=roles)

            if not is_email_exist(email):
                flash('El correo electrónico no existe')
                return render_template('admin/registrar_users.html', roles=roles)
            if 'foto_perfil' in request.files:
                foto_perfil = request.files['foto_perfil']
                if foto_perfil.filename != '':
                    # Asegúrate de que el directorio static/images existe
                    upload_folder = os.path.join(current_app.root_path, 'static/images')
                    if not os.path.exists(upload_folder):
                        os.makedirs(upload_folder)
                    file_path = os.path.join(upload_folder, foto_perfil.filename)
                    foto_perfil.save(file_path)
                    foto_perfil_path = 'images/' + foto_perfil.filename

            email_name = Usuario.query.filter_by(email=email).first()

            if email_name is None:
                rol = Roles.query.filter_by(nombre_rol=role).first()

                if not rol:
                    flash('El rol no existe')
                    return render_template('admin/registrar_users.html', roles=roles)
                user = Usuario(email=email, password=generate_password_hash(password), id_role=rol.id_rol,
                               foto_perfil=foto_perfil_path)
                db.session.add(user)
                db.session.commit()  # Commit the session to get the user ID

                # Obtener el ID del usuario recién creado
                user_id = user.id_user

                lider_add = Lider(nombres=nombre, apellidos=apellido, celular=celular, capitan_id=None,
                                  id_rol=rol.id_rol, id_user_app=user_id, direccion=direccion
                                  , pais=pais, nacimiento=nacimiento, ciudad=ciudad)

                db.session.add(lider_add)
                db.session.commit()
                return redirect(url_for('registrar.registrarVotantes'))
            else:
                flash(f'El email de usuario ya está registrado: {email_name.email}')
                return render_template('admin/registrar_users.html', roles=roles)

        except Exception as e:
            flash(f"Error del servidor 500: {e}")
            return render_template('admin/registrar_users.html', roles=roles)

    return render_template('admin/registrar_users.html', roles=roles)


@registrar_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_admin():
    user_id = session.get('user_id')
    from App.models.User import Usuario
    from App.models.sistemaModel import Lider

    from App import db

    user = Usuario.query.get(user_id)  # Obtener el usuario actual

    Lider_user = Lider.query.filter_by(id_user_app=user.id_user).first()
    if request.method == 'POST':
        updated = False  # Bandera para verificar si hay cambios

        # Obtener datos del formulario
        email = request.form['email']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        celular = request.form['celular']
        nacimiento = datetime.strptime(request.form['nacimiento'], '%Y-%m-%d') if request.form['nacimiento'] else None
        pais = request.form['pais']
        direccion = request.form['direccion']
        ciudad = request.form['ciudad']

        # Verificar si hay cambios en los datos del usuario
        if user.email != email:
            user.email = email
            updated = True

        if Lider_user.nombres != nombre:
            Lider_user.nombres = nombre
            updated = True

        if Lider_user.apellidos != apellido:
            Lider_user.apellidos = apellido
            updated = True

        if Lider_user.celular != celular:
            Lider_user.celular = celular
            updated = True

        if Lider_user.nacimiento != nacimiento:
            Lider_user.nacimiento = nacimiento
            updated = True

        if Lider_user.pais != pais:
            Lider_user.pais = pais
            updated = True

        if Lider_user.direccion != direccion:
            Lider_user.direccion = direccion
            updated = True

        if Lider_user.ciudad != ciudad:
            Lider_user.ciudad = ciudad
            updated = True

        # Manejar la carga de la foto de perfil
        if 'foto_perfil' in request.files:
            foto_perfil = request.files['foto_perfil']
            if foto_perfil.filename != '':
                upload_folder = os.path.join(current_app.root_path, 'static/images')
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                file_path = os.path.join(upload_folder, foto_perfil.filename)
                foto_perfil.save(file_path)
                user.foto_perfil = 'images/' + foto_perfil.filename
                updated = True

        # Manejar el cambio de contraseña
        new_password = request.form['new-password']
        confirm_password = request.form['confirm-password']
        if new_password and confirm_password:
            if new_password == confirm_password:
                user.password = generate_password_hash(new_password)
                updated = True
            else:
                flash('Las contraseñas no coinciden', 'danger')
                return redirect(url_for('registrar.registrarVotantes'))
        # Solo realizar la actualización si hay cambios
        if updated:
            try:
                db.session.commit()
                flash('Actualización completa!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Error actualizando el perfil: ' + str(e), 'danger')
        else:
            flash('No se realizaron cambios.', 'info')

        return redirect(url_for('registrar.registrarVotantes'))

    user_foto_perfil = user.foto_perfil if user.foto_perfil else 'images/messages-1.jpg'
    return render_template('admin/perfil.html', user=user, Lider_user=Lider_user, user_foto_perfil=user_foto_perfil)


@registrar_bp.route('/gestion', methods=('GET', 'POST'))
@login_required
def gestion_municipio():
    from App.models.sistemaModel import Municipio, Comuna, Barrio, PuestoVotacion
    from App import db

    if request.method == 'POST':
        municipio_nombre = request.form.get('Municipio')
        comuna_nombre = request.form.get('Comuna')
        barrio_nombre = request.form.get('Barrio')
        nombre_puestoV = request.form.get('nombre_votacion')
        direccion = request.form.get('direccion')

        # Validar si el municipio existe
        municipio = Municipio.query.filter_by(nombre=municipio_nombre).first()
        if municipio is None:

            municipio_add = Municipio(nombre=municipio_nombre)
            db.session.add(municipio_add)
            db.session.commit()

            id = municipio_add.id_municipio

            # Guardar el ID del municipio para la comuna
            comuna = Comuna(nombre=comuna_nombre, municipio_id=id)
            db.session.add(comuna)
            db.session.commit()

            # Obtener el ID de la comuna recién creada
            comuna_id = comuna.id_comuna

            # Guardar el barrio asociado a la comuna
            barrio = Barrio(nombre=barrio_nombre, comuna_id=comuna_id)
            db.session.add(barrio)
            db.session.commit()

            puesto = PuestoVotacion(nombre=nombre_puestoV, direccion=direccion, municipio_id=id)
            db.session.add(puesto)
            db.session.commit()

            flash('Municipio, Comuna y Barrio registrados correctamente')
        else:
            flash('El municipio ya existe')

    return render_template('admin/gestion.html')


@registrar_bp.route('/asignar', methods=('GET', 'POST'))
@login_required
def asignar():
    from App.models.sistemaModel import Comuna, Capitan, CapitanComuna
    from App import db

    comuna = Comuna.query.all()

    if request.method == 'POST':
        nombre = request.form.get('Nombre')
        apellido = request.form.get('Apellido')
        celular = request.form.get('Celular')
        comuna_id = request.form.get('comuna')
        capitan = Capitan(nombres=nombre, apellidos=apellido, celular=celular)
        db.session.add(capitan)
        db.session.commit()
        capita_id = capitan.id_capitan

        capitana_comuna = CapitanComuna(comuna_id=comuna_id, capitan_id=capita_id)
        db.session.add(capitana_comuna)
        db.session.commit()

    return render_template('admin/asignar_capitanes.html', comuna=comuna)


@registrar_bp.route('/asignar_lideres', methods=('GET', 'POST'))
@login_required
def asignar_lideres():
    from App.models.sistemaModel import Lider, CapitanComuna, Barrio, LiderRespBarrios, Capitan
    from App import db
    lider_all = Lider.query.all()
    capitana_comuna = CapitanComuna.query.all()
    bario_all = Barrio.query.all()

    capitan = db.session.query(CapitanComuna, Capitan).join(Capitan,
                                                            CapitanComuna.capitan_id == Capitan.id_capitan).all()
    if request.method == 'POST':
        Lider_id = request.form.get('lider')
        CapitanComuna_id = request.form.get('Capitan')
        Barrio_id = request.form.get('barrio')

        lider = LiderRespBarrios(lider_id=Lider_id, capitancomuna_id=CapitanComuna_id, barrio_id=Barrio_id)
        db.session.add(lider)
        db.session.commit()

    return render_template('admin/asignar_lideres.html', lider=lider_all, capitanacomuna=capitana_comuna,
                           capitan1=capitan,
                           barrio=bario_all)
