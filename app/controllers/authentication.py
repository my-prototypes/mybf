from flask import Blueprint
from flask import session, request, redirect, url_for, render_template, flash
from app.forms import LoginForm
from werkzeug.security import check_password_hash, generate_password_hash
from app.extensions import db, login_manager
from flask_login import logout_user

# Evita importacao de dependencia circular
from ..dao import UserDAO
from ..models import User

userDAO = UserDAO(db)

auth_bp = Blueprint('auth', __name__, template_folder='app/templates')

@login_manager.user_loader 
def load_user(user_id):
    return userDAO.user_by_id(user_id)

@login_manager.unauthorized_handler 
def unauthorized_callback():
    return redirect(url_for("auth.login"))

@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = userDAO.user_by_username(username)
        if not user:
            flash("That username does not exist, please try again.")
            return redirect(url_for('auth.login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.') 
            return redirect(url_for('auth.login'))
        msg = 'Usuário logado com sucesso!'
        flash(msg, category='success')
        session['username'] = username
        return redirect(url_for('dashboard.dashboard_page'))

    if login_form.errors != {}: #If there are not errors from the validations
        for err_msg in login_form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template("auth/login.html", form=login_form)

# Pagina de registro
@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    """
    Register a new user.
    Validates that the username is not already taken. Hashes the password for security.
    """
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        error = None
        
        resultado_busca = userDAO.user_by_username(username=username)

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif (resultado_busca is not None):
            error = f"User {username} is already registered."

        if error is None:
            # the name is available, store it in the database and go to the login page
            hash_and_salted_password = generate_password_hash(password)
            usuario = User(name=name, username=username, email=email, password=hash_and_salted_password)
            userDAO.create_user(user=usuario)
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")

# Pagina de recuperacao de e-mail
@auth_bp.route("/forgot-password", methods=["GET"])
def forgot():
    return render_template("auth/forgot-password.html")

@auth_bp.route('/logout') 
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('auth.login'))