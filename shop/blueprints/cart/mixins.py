from flask import session
from flask import request

from .utils import CartObj
from blueprints.core.models import Variant

class CartMixin:
    event = None
    product_model = Variant

    def dispatch_request(self, *args, **kwargs):
        self.cart = CartObj(session)
        self.extra_context = {'cart_obj': self.cart}
        return super().dispatch_request(*args, **kwargs)

    def cart_dispatch(self, event, *args):
        product_id = request.form.get('id')
        self.cart.action(event, product_id)
        kwargs = {'count': self.cart.count}
        if event in ['add', 'delete']:
            count = self.cart.orders.get(product_id)
            p = self.product_model.query.get(product_id)
            kwargs.update({'count_order': self.cart.count_order(product_id), 'extra': [p.count < count, p.count],
                           'price': p.price * count})
        return kwargs
