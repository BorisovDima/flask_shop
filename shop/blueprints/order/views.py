from flask import redirect, url_for, current_app, session

from blueprints.cart.mixins import CartMixin
from blueprints.core.mixins import BaseView, DetailView


from .models import OrderModel, OrderItem
from .forms import OrderForm

O_I = current_app.config['ORDER_SESSION_ID']


class OrderView(CartMixin, BaseView):

    def get(self, *args, **kwargs):
        return self.get_template({'form': OrderForm()})


    def post(self, *args, **kwargs):
        form = OrderForm()
        if not form.validate_on_submit():
            return self.get_template({'form': form})

        order = OrderModel(**form.get_order_data())
        order.set_items(self.cart)

        self.cart_dispatch('clear')
        if session.get(O_I):
            o = OrderModel.query.filter_by(id=session[O_I]).first()
            if o: o.delete()
        session[O_I] = order.id

        return redirect(url_for('order.order-pay'))


class OrderPay(BaseView):

    def get(self, *args, **kwargs):
        order_q = OrderModel.query.filter_by(id=session.get(O_I), paid=False).first_or_404()
        return self.get_template({'object': order_q})

