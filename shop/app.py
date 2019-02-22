from flask import Flask

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager
from flask_collect import Collect
import stripe


from blueprints.admin.mixins import IndexAdmin


login = LoginManager()
login.login_view = 'user.login'

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
admin = Admin(name='flask_shop', index_view=IndexAdmin(),
              base_template='admin/base_admin.html', endpoint='admin')
collect = Collect()

def make_app(config=None):
    app = Flask(__name__)
    app.config.from_pyfile('configs.py')
    stripe.api_key = app.config['STRIPE_SERCRET_KEY']

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login.init_app(app)
    admin.init_app(app)
    collect.init_app(app)
    with app.app_context():
        from blueprints.cart.routes import cart
        from blueprints.order.routes import order
        from blueprints.user.routes import user
        from blueprints.admin.routes import my_admin
        from blueprints.core.routes import core
        from blueprints.payment.routes import payment
        import errors
        import commands
        import logs

    app.register_blueprint(url_prefix='/', blueprint=core)
    app.register_blueprint(url_prefix='/', blueprint=order)
    app.register_blueprint(url_prefix='/', blueprint=user)
    app.register_blueprint(url_prefix='/', blueprint=my_admin)
    app.register_blueprint(url_prefix='/', blueprint=payment)
    app.register_blueprint(url_prefix='/api/cart/', blueprint=cart)

    collect.collect(verbose=True)
    return app


app = make_app()













