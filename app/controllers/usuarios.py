from flask import Blueprint
from flask import session, redirect, url_for, render_template, request, flash
from flask_login import login_required
from app.extensions import db

# Evita importacao de dependencia circular
from ..dao import UserDAO

userDAO = UserDAO(db)

usuarios_bp = Blueprint('user', __name__, template_folder='app/templates')

@login_required
@usuarios_bp.route("/usuario/<int:id>", methods=['GET', 'PUT'])
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