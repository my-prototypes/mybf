from .models import User, ImageProfile, File

class UserDAO:
    def __init__(self, db):
        self.db = db
        self.imagesProfile = ImageProfileDAO(db)

    def create_user(self, user):
        self.db.session.add(user)
        self.db.session.commit()

    def user_by_id(self, user_id):
        return User.query.get(user_id)

    def user_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def update_user(self, user):
        self.db.session.merge(user)
        self.db.session.commit()

    def delete_user_by_id(self, user_id):
        user = self.user_by_id(user_id)
        if user:
            self.db.session.delete(user)
            self.db.session.commit()

    def list_users(self):
        return User.query.all()

    def add_profile_image_to_user(self, image):
        try: 
            if not self.imagesProfile.get_image_profile_for_user(image.user_id): 
                self.db.session.add(image)
                self.db.session.commit()
            else:
                self.db.session.merge(image)
                self.db.session.commit()
        except ValueError:
            raise ValueError('Erro ao adicionar imagem de profile')

    def link_to_file(self, user_id, file):
        try:
            user = User.query.filter_by(id=user_id).first()
            file = File.query.filter_by(id=file.id).first()
            user.my_files.append(file)
            self.db.session.commit()
        except ValueError as ve:
            raise ValueError(f'Error during file to user - {ve}')

    def link_to_files(self, user_id, files):
        try:
            user = User.query.filter_by(id=user_id).first()
            for each in files:
                file = File.query.filter_by(id=each.id).first()
                user.my_files.append(file)    
            self.db.session.commit()
        except ValueError as ve:
            raise ValueError(f'Error during files to user - {ve}')

    def unlink_file(self, user_id, file):
        try:
            user = User.query.filter_by(id=user_id).first()
            file = File.query.filter_by(id=file.id).first()
            user.my_files.remove(file)
            self.db.session.commit()
        except Exception as e:
            raise Exception(f'Error during remove file from user - {e}')

    def list_all_files(self, user_id):
        user = User.query.filter_by(id=user_id).first()        
        return user.my_files

    def get_file_by_user(self, name):        
        return User.my_files.query.get(name)


class ImageProfileDAO:
    def __init__(self, db):
        self.db = db

    def create_image_profile(self, image):
        self.db.session.add(image)
        self.db.session.commit()

    def get_image_profile_for_user(self, user_id):
        return ImageProfile.query.get(user_id)

    def get_all_image_profile(self):
        return ImageProfileDAO.query.all()


class FilesDAO:
    def __init__(self, db):
        self.db = db

    def insert_file(self, file):
        try:
            self.db.session.add(file)
            self.db.session.commit()
        except ValueError as ve:
            raise ValueError(f'Error during insert file - {ve}')

    def query_file_by_name(self, p_name):
        file = File.query.filter_by(name=p_name).first()
        return file

    def query_file_by_id(self, p_id):
        file = File.query.filter_by(id=p_id).first()
        return file
    
    def list_all_files(self):
        return File.query.all()

    def delete_file(self, file):
        try:
            file = File.query.filter_by(id=file.id).first()
            self.db.session.delete(file)
            self.db.session.commit()
        except ValueError as ve:
            raise ValueError(f'Error during delete file - {ve}')