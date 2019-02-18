from flask import Blueprint
from .views import OrderView, OrderPay


order = Blueprint('order', __name__, template_folder='templates')

order.add_url_rule('/order/', view_func=OrderView.as_view('order-form', template_name='order/order_form.html'))
order.add_url_rule('/order/payment/', view_func=OrderPay.as_view('order-pay', template_name='order/order_payment.html'))