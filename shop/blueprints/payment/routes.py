from flask import Blueprint
from .views import StripePay, SuccessView

payment = Blueprint('payment', __name__, template_folder='templates')

payment.add_url_rule('/payment/charge/', view_func=StripePay.as_view('pay-stripe'))


payment.add_url_rule('/payment/done/', view_func=SuccessView.as_view('success-pay', template_name='payment/success.html'))





