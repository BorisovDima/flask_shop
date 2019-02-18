from flask import Blueprint
from . import views

user = Blueprint('user', __name__, template_folder='templates')

user.add_url_rule('/login/', view_func=views.LoginView.as_view('login', template_name='user/authorization.html'))
user.add_url_rule('/logout/', view_func=views.LogoutView.as_view('logout'))
