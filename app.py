import os 

from flask import Flask, send_from_directory, render_template, request, url_for, redirect, flash 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

app = Flask(__name__, template_folder='templates')

STATIC_PATH = os.path.join(app.root_path, 'static')

app.config['SECRET_KEY'] = "python is the real deal !@#$%"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.static_folder = STATIC_PATH

db = SQLAlchemy(app)

login_manager = LoginManager() 
login_manager.init_app(app)

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False) 
    password = db.Column(db.String(500), nullable=False)

class LoginForm(FlaskForm):
    username = StringField()
    password = PasswordField()
    submit = SubmitField('Logar')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(STATIC_PATH, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def hello_world():
    print('Bem vindo ao Flask!')
    return render_template('home.html')

@login_manager.user_loader 
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler 
def unauthorized_callback():
    return redirect(url_for("login"))

@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        print(username, password)
        user = User.query.filter_by(username=username).first()
        if not user:
            flash("That username does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.') 
            return redirect(url_for('login'))
        msg = 'Usuário logado com sucesso!'
        flash(msg, category='success')
        return redirect(url_for('dashboard_page'))

    if login_form.errors != {}: #If there are not errors from the validations
        for err_msg in login_form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template("auth/login.html", form=login_form)

# Pagina de registro
@app.route("/register", methods=['GET', 'POST'])
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
        resultado_busca = User.query.filter_by(username=username).first()

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif (resultado_busca is not None):
            error = f"User {username} is already registered."

        if error is None:
            # the name is available, store it in the database and go to the login page
            #usuario = Usuario(id=1, fullname=name, email=email, username=username, password=password)
            #usuario_dao.cadastrar_usuario(usuario)
            return redirect(url_for("login"))

        flash(error)

    return render_template("auth/register.html")

# Pagina de recuperacao de e-mail
@app.route("/forgot-password", methods=["GET"])
def forgot():
    return render_template("auth/forgot-password.html")

@app.route('/dashboard')
def dashboard_page():
    #repositories = Repository.query.filter_by(owner=current_user.get_id()).all()
    usuarios = []
    imagens = []
    quantidade_usuarios = 1
    quantidade_imagens = 0
    print('Carrega os dados do usuário logado')
    return render_template("dashboard/starter.html", usuario = 'armando', profilePic="", titulo="Dashboard", usuarios = usuarios, imagens = imagens, quantidade_usuarios=quantidade_usuarios, quantidade_imagens=quantidade_imagens) 

@app.route('/logout') 
def logout():
    logout_user()
    return redirect(url_for('login'))

with app.app_context():
    print('Cria as tabelas do banco')
    db.drop_all()
    db.create_all()
    print('Create a test user')
    hash_and_salted_password = generate_password_hash('armando')
    new_user = User(username='armando', password=hash_and_salted_password)
    db.session.add(new_user)
    db.session.commit()