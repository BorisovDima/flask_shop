from flask import request, redirect, url_for
from flask import current_app

from blueprints.core.mixins import BaseView
from blueprints.order.models import OrderModel
from app import stripe
from flask import session

O_I = current_app.config['ORDER_SESSION_ID']



class StripePay(BaseView):

    def post(self, *args, **kwargs):
        order = OrderModel.query.filter_by(id=session.pop(O_I, None)).first_or_404()
        customer = stripe.Customer.create(
            email='customer@example.com',
            source=request.form['stripeToken']
        )
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=order.total_price * 100,
            currency='usd',
            description='Flask Charge'
        )
        order.make_sales()
        return redirect(url_for('payment.success-pay'))





class SuccessView(BaseView):
    def get(self, *args, **kwargs):
        return self.get_template({})



