from flask import Blueprint
from flask import session, redirect, url_for, render_template, request, flash
from flask_login import login_required
from app.extensions import db
from app.utils.utilidades import Constant
import os
from werkzeug.utils import secure_filename

# Evita importacao de dependencia circular
from ..dao import UserDAO
from ..models import Image

userDAO = UserDAO(db)

usuarios_bp = Blueprint('user', __name__, template_folder='app/templates')

# Cria o diretorio do usuario caso nao exista
def user_directory(path_temp, user_id, sub_folder=None):
    if sub_folder is not None: 
        user_path = path_temp + '/' + str(user_id) + '/' + sub_folder
    else:
        user_path = path_temp + '/' + str(user_id)

    if os.path.exists(user_path):
        return user_path
    else: 
        os.makedirs(user_path)
    return user_path 

@usuarios_bp.route("/usuarios")
def listar_usuarios():
    usuarios = userDAO.list_users()
    return render_template('usuarios/listar_usuarios.html', usuarios=usuarios)

@login_required
@usuarios_bp.route("/usuarios/<int:id>/profile/imagem", methods=['GET', 'POST'])
def update_image(id):    
    if request.method == "POST":
        username = request.form["username"]
        file_image = request.files["image"]
        # Pega o nome da imagem
        file_name_to_store = secure_filename(file_image.filename)
        profile = 1
        image = Image(name=file_name_to_store, type_image=profile)
        userDAO.add_image_to_user(id, image)
        error = None
        if not username:
            error = "Username is required."

        if error is not None:
            flash(error)
        else:
            try:
                print('Processamento do upload da imagem')
                # Cria o diretorio de profile do usuario, caso ele nao exista
                user_img_directory = user_directory(path_temp=Constant.PATH_IMG, user_id=id, sub_folder="profile")
                path_to_save = user_img_directory + "/" + file_name_to_store
                # Salva o arquivo no diretorio de uploads
                file_image.save(path_to_save)
                print(f'Arquivo {file_name_to_store} salvo com sucesso!')
                print(f'Local: {path_to_save}')
            except:
                error_processing_upload = "Erro no processamento do upload do processamento da imagem."
                if error_processing_upload is not None:
                    flash(error_processing_upload, 'danger')
                    return redirect(url_for("usuario.listar_usuarios"))
            message = "Imagem do usuário atualizada com sucesso!"
            flash(message, 'success')            
            filename_picture = 'img/' + str(id) + '/' + file_name_to_store
            return redirect(url_for("dashboard.profile", filename=filename_picture))

    usuario = userDAO.user_by_username(username=session['username'])
    profile = 1
    image_profile = userDAO.get_image_profile_for_user(usuario.id, profile)
    if image_profile: 
        filename_picture = 'img' + '/' + str(usuario.id) + '/' + 'profile' + '/' + image_profile.name
    else: 
        filename_picture = 'dist/img/anonymous2.png'
    return render_template("usuarios/imagem.html", usuario = session['username'], 
            profilePic="", titulo="Update image", usuario_logado=session['username'], id=id, nome=usuario.username, filename=filename_picture)