from flask import Blueprint, render_template, request, url_for, redirect, flash, current_app, session, jsonify
from App.controllers.AuthController import login_required

informacion_bp = Blueprint('informacion', __name__, url_prefix='/informacion')


@informacion_bp.route('/informacionVotantes', methods=('GET', 'POST'))
@login_required
def registrarVotantes():
    from App.models.User import Usuario
    from App.models.sistemaModel import DatosVotante, Lider

    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('auth.login'))

    user = Usuario.query.get(user_id)
    rol = user.id_rol

    if rol != 1:
        lider = Lider.query.filter_by(id_user_app=user.id_user).first()
        if lider:
            datos = DatosVotante.query.filter_by(lider_id=lider.id_lider).all()
        else:
            datos = []
    else:
        datos = DatosVotante.query.all()
        lider = None

    return render_template('admin/informacion.html', rol=rol, datos=datos, lider=lider)


@informacion_bp.route('/eliminar_votante/<int:id>', methods=['POST'])
@login_required
def eliminar_votante(id):
    from App.models.sistemaModel import DatosVotante
    from App import db

    votante = DatosVotante.query.get_or_404(id)
    db.session.delete(votante)
    db.session.commit()
    flash('Votante eliminado exitosamente', 'success')
    return redirect(url_for('informacion.registrarVotantes'))


@informacion_bp.route('/editar_votante/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_votante(id):
    from App.models.sistemaModel import DatosVotante

    from App import db

    votante = DatosVotante.query.get_or_404(id)
    if request.method == 'POST':
        votante.nombres = request.form['nombres']
        votante.apellidos = request.form['apellidos']
        votante.direccion = request.form['direccion']
        votante.telefono = request.form['telefono']
        votante.cedula = request.form['cedula']
        votante.mesa = request.form['mesa']
        # Aquí puedes agregar más campos según tu modelo

        db.session.commit()
        flash('Votante actualizado exitosamente', 'success')
        return redirect(url_for('informacion.registrarVotantes'))

    return render_template('admin/editar_votante.html', votante=votante)
