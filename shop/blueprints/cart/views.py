from .mixins import CartMixin
from blueprints.core.mixins import WrapJsonMixin, BaseView



class CartView(WrapJsonMixin, CartMixin, BaseView):

    def get(self, *args, **kwargs):
       return {'html':self.get_template(self.extra_context)}


    def post(self, *args, **kwargs):
        return self.cart_dispatch(self.event)


