import os 
from flask import Flask, send_from_directory, render_template, request, url_for, redirect, flash 
from flask_login import UserMixin, LoginManager, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from app.forms import LoginForm
from flask import session

app = Flask(__name__, template_folder='app/templates')

app.config['SECRET_KEY'] = "python is the real deal !@#$%"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

STATIC_PATH = os.path.join(app.root_path, 'app/static')

db = SQLAlchemy(app)

# Evita importacao de dependencia circular
from app.dao import UserDAO
from app.models import User

userDAO = UserDAO(db)

app.static_folder = STATIC_PATH

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(STATIC_PATH, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def hello_world():
    print('Bem vindo ao Flask!')
    return render_template('home.html')

@login_manager.user_loader 
def load_user(user_id):
    return userDAO.read_user_by_id(user_id)

@login_manager.unauthorized_handler 
def unauthorized_callback():
    return redirect(url_for("login"))

@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = userDAO.read_user_by_username(username)
        if not user:
            flash("That username does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.') 
            return redirect(url_for('login'))
        msg = 'Usuário logado com sucesso!'
        flash(msg, category='success')
        session['username'] = username
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
        
        resultado_busca = userDAO.read_user_by_username(username=username)

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
            return redirect(url_for("login"))

        flash(error)

    return render_template("auth/register.html")

# Pagina de recuperacao de e-mail
@app.route("/forgot-password", methods=["GET"])
def forgot():
    return render_template("auth/forgot-password.html")

@app.route('/logout') 
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))

@login_required
@app.route('/dashboard')
def dashboard_page():
    if 'username' not in session: 
        return redirect(url_for('login'))

    usuarios = userDAO.list_users()
    imagens = []
    quantidade_usuarios = len(usuarios)
    quantidade_imagens = len(imagens)
    
    return render_template("dashboard/starter.html", usuario = session['username'], 
            profilePic="", titulo="Dashboard", usuarios = usuarios, 
            imagens = imagens, quantidade_usuarios=quantidade_usuarios, 
            quantidade_imagens=quantidade_imagens) 

@login_required
@app.route("/profile")
def profile():
    if 'username' not in session: 
        return redirect(url_for('login'))

    usuario = userDAO.read_user_by_username(username=session['username'])
    return render_template("dashboard/profile.html", usuario = session['username'], 
            profilePic="", titulo="Profile", nome=usuario.name, id=str(usuario.id), email=usuario.email)

@login_required
@app.route("/usuario/<int:id>", methods=['GET', 'PUT'])
def update(id):    
    if request.method == "POST":
        username = request.form["username"]
        #file_name_to_store = "picture-" + str(id) + ".png" 
        error = None

        if not username:
            error = "Username is required."

        if error is not None:
            flash(error)
        else:
            try:
                print('Processamento do upload da imagem')
                # TO DO: isolar o tratamento de arquivo
                #file_image = request.files["image"]
                #path_to_save = Constant.PATH_UPLOADS + "/" + file_name_to_store
                # Salva o arquivo no diretorio de uploads
                #file_image.save(path_to_save)
            except:
                error_processing_upload = "Erro no processamento do upload do processamento da imagem."
                if error_processing_upload is not None:
                    flash(error_processing_upload, 'danger')
                    return redirect(url_for("usuario.listar_usuarios"))
            message = "Usuario atualizado com sucesso!"
            flash(message, 'success')
            return redirect(url_for("dashboard.profile"))

    usuario = userDAO.read_user_by_username(username=session['username'])

    return render_template("usuarios/imagem.html", usuario = session['username'], 
            profilePic="", titulo="Update image", usuario_logado=session['username'], nome=usuario.username)

# Recria as tabelas do banco
#with app.app_context():
#    print('Cria as tabelas do banco')
#    db.create_all()
#    print('Tabelas criadas com sucesso!')