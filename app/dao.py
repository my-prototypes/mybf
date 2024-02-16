from .models import User, ImageProfile

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

    # image = Image(name="MyImage.jpg", type_image=1)
    # type 1 - profile
    # type 2 - arquivos 
    # user.images.append(image)
    def add_image_to_user(self, user_id, image):
        user = self.user_by_id(user_id)
        image.user = user
        self.db.session.add(image)
        self.db.session.commit()
        self.update_user(user)

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

    def get_all_images_for_user(self, user_id):
        user = self.user_by_id(user_id)
        return user.images.all()

    # TODO: falta atualizar o user
    def remove_image_from_user(self, user_id, image_id):
        user = self.user_by_id(user_id)
        image = user.images.filter_by(id=image_id).first()
        if image:
            self.db.session.delete(image)
            self.db.session.commit()
            return True
        else:
            return False

    # TODO: falta atualizar o user
    def update_image_for_user(self, user_id, image_id, new_name, new_type):
        user = self.user_by_id(user_id)
        image = user.images.filter_by(id=image_id).first()
        if image:
            image.name = new_name
            image.type_image = new_type
            self.db.session.merge(image)
            self.db.session.commit()
            return True
        else:
            return False

    def get_images_for_user(self, user_id, type_image):
        user = self.user_by_id(user_id)

        return user.images.filter_by(type_image=type_image).first()

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

