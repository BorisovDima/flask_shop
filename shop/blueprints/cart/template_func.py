from .utils import CartObj
from flask import session
from .routes import cart

@cart.app_template_global()
def cart_count():
    cart = CartObj(session)
    return cart.count


