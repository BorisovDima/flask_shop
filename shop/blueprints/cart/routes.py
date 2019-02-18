from flask import Blueprint
from .views import CartView

cart = Blueprint('cart', __name__, template_folder='templates')

cart.add_url_rule('/put/', view_func=CartView.as_view('put', event='add'))
cart.add_url_rule('/delete/', view_func=CartView.as_view('delete', event='delete'))

cart.add_url_rule('/delete-all/', view_func=CartView.as_view('delete-all', event='delete_all'))
cart.add_url_rule('/check/', view_func=CartView.as_view('check', template_name='cart/objects/cart_object.html'))

from .template_func import cart_count
