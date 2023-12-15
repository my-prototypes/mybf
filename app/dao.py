from .models import User

class UserDAO:
    def __init__(self, db):
        self.db = db

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