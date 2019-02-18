from flask_login import UserMixin
from blueprints.core.model_mixins import BaseShopMixin, db
from app import login

from werkzeug.security import generate_password_hash, check_password_hash



class UserModel(UserMixin, BaseShopMixin):
    password = db.Column(db.String(1024), nullable=False)
    name = db.Column(db.String(50), nullable=False, unique=True)
    is_staff = db.Column(db.Boolean, default=False)
    is_superuser = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(64))

    def set_password(self, pswd):
        self.password = generate_password_hash(pswd)

    def check_password(self, pswd):
        return check_password_hash(self.password, pswd)


@login.user_loader
def LoadUser(user_id):
    return UserModel.query.get(user_id)
