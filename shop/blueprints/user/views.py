from flask_login import login_user, logout_user, login_required, current_user
from flask import redirect, url_for, current_app

from .forms import LoginForm
from .utils import not_login_required
from blueprints.core.mixins import BaseView



class LoginView(BaseView):
    methods = ['GET', 'POST']
    decorators = [not_login_required]

    def dispatch_request(self, *args, **kwargs):
        form = LoginForm()
        if form.validate_on_submit():
            login_user(form.login_user_instance)
            current_app.logger.info('User %s logged in' % form.login_user_instance.name)
            return redirect(url_for('admin.index'))
        return self.get_template({'form': form})


class LogoutView(BaseView):
    methods = ['POST']
    decorators = [login_required]

    def dispatch_request(self, *args, **kwargs):
        current_app.logger.info('User %s logout' % current_user.name)
        logout_user()
        return redirect(url_for('core.mainpage'))
