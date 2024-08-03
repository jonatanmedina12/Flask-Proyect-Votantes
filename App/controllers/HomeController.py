from flask import Blueprint, render_template
from App.controllers.AuthController import login_exist

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
@login_exist
def index_home():
    return render_template('index.html')
