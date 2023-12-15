from flask import Blueprint
from flask import session, redirect, url_for, render_template
from flask_login import login_required
from app.extensions import db

# Evita importacao de dependencia circular
from ..dao import UserDAO

userDAO = UserDAO(db)

dashboard_bp = Blueprint('dashboard', __name__, template_folder='app/templates')

@dashboard_bp.route('/dashboard')
def dashboard_page():
    if 'username' not in session: 
        return redirect(url_for('auth.login'))

    usuarios = userDAO.list_users()
    imagens = []
    quantidade_usuarios = len(usuarios)
    quantidade_imagens = len(imagens)

    usuario = userDAO.user_by_username(username=session['username'])
    profile = 1
    image_profile = userDAO.get_image_profile_for_user(usuario.id, profile)
    if image_profile: 
        filename_picture = 'img' + '/' + str(usuario.id) + '/' + 'profile' + '/' + image_profile.name
    else: 
        filename_picture = 'dist/img/anonymous2.png'

    
    return render_template("dashboard/starter.html", usuario = session['username'], 
            profilePic="", titulo="Dashboard", usuarios = usuarios, 
            imagens = imagens, quantidade_usuarios=quantidade_usuarios, 
            quantidade_imagens=quantidade_imagens, filename=filename_picture) 

@login_required
@dashboard_bp.route("/profile")
def profile():
    if 'username' not in session: 
        return redirect(url_for('login'))

    usuario = userDAO.user_by_username(username=session['username'])
    profile = 1
    image_profile = userDAO.get_image_profile_for_user(usuario.id, profile)
    if image_profile: 
        filename_picture = 'img' + '/' + str(usuario.id) + '/' + 'profile' + '/' + image_profile.name
    else: 
        filename_picture = 'dist/img/anonymous2.png'

    return render_template("dashboard/profile.html", usuario = session['username'], 
            profilePic="", titulo="Profile", nome=usuario.name, id=str(usuario.id), email=usuario.email, filename=filename_picture)