import os 
from flask import Flask, send_from_directory, render_template
from app.extensions import db, login_manager
from app.controllers.dashboard import dashboard_bp
from app.controllers.authentication import auth_bp
from app.controllers.usuarios import usuarios_bp
from app.dao import UserDAO

app = Flask(__name__, template_folder='app/templates')

STATIC_PATH = os.path.join(app.root_path, 'app/static')

app.config['SECRET_KEY'] = "python is the real deal !@#$%"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.static_folder = STATIC_PATH

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"

# Register Blueprints
app.register_blueprint(dashboard_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(usuarios_bp)

userDAO = UserDAO(db)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(STATIC_PATH, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def hello():
    print('Bem vindo ao Flask!')        
    print('Lista de recursos disponíveis: ')
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = str(rule.endpoint) + ' - '+ str(methods) + ' - '+ str(rule)
        output.append(line)

    for line in sorted(output):
        print(line)

    return render_template('home.html')

# Recria as tabelas do banco
def create_tables():
    with app.app_context():
        print('Cria as tabelas do banco')
        db.create_all()
        print('Tabelas criadas com sucesso!')

if __name__=='__main__':
    app.run()