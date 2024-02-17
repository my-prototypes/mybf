from flask import Blueprint
from flask import session, redirect, url_for, render_template, request, flash, send_from_directory
from flask_login import login_required
from app.extensions import db
from app.utils.utilidades import Constant
import os
from werkzeug.utils import secure_filename
from PIL import Image

# Evita importacao de dependencia circular
from ..dao import UserDAO, ImageProfileDAO, FilesDAO
from ..models import ImageProfile, File

userDAO = UserDAO(db)
imageProfileDAO = ImageProfileDAO(db)
fileDAO = FilesDAO(db)

usuarios_bp = Blueprint('user', __name__, template_folder='app/templates')

# dado um arquivo cria o thumbnail correspondente e salva na pasta de thumbnails
def tnails(filename, filename_path, thumbnail_path):
    try:
        filename_complete = filename_path + '/' + filename
        image = Image.open(filename_complete)
        image.thumbnail((90,90))        
        new_thumbnail = thumbnail_path + '/' + filename
        image.save(new_thumbnail)
    except IOError as io:
        raise Exception(f'Erro - {io}')

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
    user = userDAO.user_by_username(session['username'])
    image_profile = imageProfileDAO.get_image_profile_for_user(user.id)

    id = str(user.id)

    filename_picture = None
    if image_profile: 
        filename_picture = 'img' + '/' + id + '/' + 'profile' + '/' + image_profile.name
        print(f"filename_picture: {filename_picture}")
    else: 
        filename_picture = 'dist/img/anonymous2.png'

    return render_template('usuarios/listar_usuarios.html', usuarios=usuarios, usuario=session['username'], 
    titulo="Lista de Usuários", usuario_logado=session['username'], id=id, filename=filename_picture)

@login_required
@usuarios_bp.route("/usuarios/<int:id>/profile/imagem", methods=['GET', 'POST'])
def update_image(id):    
    if request.method == "POST":
        username = request.form["username"]
        file_image = request.files["image"]
        try:
            # Pega o nome da imagem
            file_name_to_store = secure_filename(file_image.filename)
            image = ImageProfile(user_id=id, name=file_name_to_store)
            userDAO.add_profile_image_to_user(image)
            print('Processamento do upload da imagem')
            # Cria o diretorio de profile do usuario, caso ele nao exista
            user_img_directory = user_directory(path_temp=Constant.PATH_IMG, user_id=id, sub_folder="profile")
            path_to_save = user_img_directory + "/" + file_name_to_store
            # Salva o arquivo no diretorio de uploads
            file_image.save(path_to_save)
            print(f'Arquivo {file_name_to_store} salvo com sucesso!')
            print(f'Local: {path_to_save}')
        except ValueError as vex:
            erro = str(vex)
            print(f'Erro: {erro}')
            flash(erro)
            return redirect(url_for("dashboard.profile", filename=file_name_to_store))
        except:
            error_processing_upload = "Erro no processamento do upload do processamento da imagem."
            flash(error_processing_upload, 'danger')
            return redirect(url_for("usuario.listar_usuarios"))
        
        message = "Imagem do usuário atualizada com sucesso!"
        flash(message, 'success')            
        filename_picture = 'img/' + str(id) + '/' + file_name_to_store
        return redirect(url_for("dashboard.profile", filename=filename_picture))

    usuario = userDAO.user_by_username(username=session['username'])
    image_profile = imageProfileDAO.get_image_profile_for_user(usuario.id)
    if image_profile: 
        filename_picture = 'img' + '/' + str(usuario.id) + '/' + 'profile' + '/' + image_profile.name
    else: 
        filename_picture = 'dist/img/anonymous2.png'
    return render_template("usuarios/imagem.html", usuario = session['username'], 
            profilePic="", titulo="Update image", usuario_logado=session['username'], id=id, nome=usuario.username, filename=filename_picture)

@login_required
@usuarios_bp.route("/usuarios/<int:id>/upload/imagem", methods=['GET', 'POST'])
def upload_image(id):    
    file_name_to_store = None
    if request.method == "POST":
        file_image = request.files["image"]
        try:
            # Pega o nome da imagem
            file_name_to_store = secure_filename(file_image.filename)
            print('Processamento do upload da imagem')
            # Cria o diretorio de profile do usuario, caso ele nao exista
            user_img_directory = user_directory(path_temp=Constant.PATH_UPLOADS, user_id=id)
            path_to_save = user_img_directory + "/" + file_name_to_store
            # Salva o arquivo no diretorio de uploads
            file_image.save(path_to_save)
            file_to_save = File(name=file_name_to_store)
            fileDAO.insert_file(file_to_save)
            path_to_save_image_thumbnail = user_directory(Constant.PATH_UPLOADS_THUMBNAILS, id)
            tnails(file_name_to_store, user_img_directory, path_to_save_image_thumbnail)
            userDAO.link_to_file(user_id=id, file=file_to_save)
            print(f'Arquivo {file_name_to_store} salvo com sucesso!')
            print(f'Local: {path_to_save}')
        except:
            error_processing_upload = "Erro no processamento do upload do processamento da imagem."
            flash(error_processing_upload, 'danger')
            return redirect(url_for("usuario.listar_usuarios"))

    if file_name_to_store: 
        filename_picture_upload = 'uploads' + '/' + str(id) + '/' + file_name_to_store
    else:
        filename_picture_upload = 'dist/img/no_image.png'

    image_profile = imageProfileDAO.get_image_profile_for_user(id)

    filename_picture = None
    if image_profile: 
        filename_picture = 'img' + '/' + str(id) + '/' + 'profile' + '/' + image_profile.name
        print(f"filename_picture: {filename_picture}")
    else: 
        filename_picture = 'dist/img/anonymous2.png'

    print(f"filename_picture: {filename_picture}")

    return render_template("usuarios/upload_imagem.html", usuario=session['username'], 
    titulo="Upload image", usuario_logado=session['username'], id=id, filename_uploaded=filename_picture_upload, filename=filename_picture)

@login_required
@usuarios_bp.route("/usuarios/<int:id>/imagens", methods=['GET'])
def lista_imagens_por_usuario(id):
    todas_as_imagens = userDAO.list_all_files(id)
    id = str(id)
    
    filename_picture = None
    usuario = userDAO.user_by_username(username=session['username'])
    image_profile = imageProfileDAO.get_image_profile_for_user(usuario.id)
    if image_profile: 
        filename_picture = 'img' + '/' + str(usuario.id) + '/' + 'profile' + '/' + image_profile.name
    else: 
        filename_picture = 'dist/img/anonymous2.png'

    return render_template("usuarios/listar_imagens.html", titulo="Minhas Imagens", usuario=session['username'], usuario_logado=session['username'], id=id, images=todas_as_imagens, filename=filename_picture)

# http://localhost:5000/usuarios/5/download/imagem/armando.jpeg
@login_required
@usuarios_bp.route('/usuarios/<int:id>/download/imagem/<name>')
def download_file(id, name):
    path_to_save_image = user_directory(Constant.PATH_UPLOADS, str(id))
    return send_from_directory(path_to_save_image, name)

