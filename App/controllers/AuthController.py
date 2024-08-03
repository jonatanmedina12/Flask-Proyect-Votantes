
from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g
from werkzeug.security import check_password_hash
from functools import wraps
from sqlalchemy.exc import OperationalError

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_exist(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.get('user') is not None:
            return redirect(url_for('registrar.registrarVotantes'))

        return view(**kwargs)

    return wrapped_view


@auth_bp.before_app_request
def load_logger_in_user():
    from App.models.User import Usuario

    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = Usuario.query.get_or_404(user_id)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.index_home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.get('user') is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view


@auth_bp.route('/login', methods=['GET', 'POST'])
@login_exist
def login():
    if g.user:
        return redirect(url_for('registrar.registrarVotantes'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:

            from App.models.User import Usuario
            from App import db

            user_name = Usuario.query.filter_by(email=email).first()
            error = None
            if user_name is None:
                error = "error"
                flash(f'Contraseña o usuario incorrectos')
            elif not check_password_hash(user_name.password, password):
                error = "error"
                flash(f'Contraseña o usuario incorrectos')
            if error is None:
                session.clear()
                session['user_id'] = user_name.id_user
                return redirect(url_for('registrar.registrarVotantes'))
        except OperationalError as e:
            flash('Hubo un problema con la conexión a la base de datos. Por favor, inténtelo de nuevo más tarde.')
            # Aquí puedes registrar el error si lo deseas.

    return render_template('Auth/login.html')
