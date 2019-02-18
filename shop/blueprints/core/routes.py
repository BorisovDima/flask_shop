from flask import Blueprint

from .views import MainPageView, DetailProductView

core = Blueprint('core', __name__, template_folder='templates')


core.add_url_rule(rule='/', view_func=MainPageView.as_view('mainpage',
                                                template_name='core/mainpage.html'))

core.add_url_rule(rule='/detail/<name>/', view_func=DetailProductView.as_view('detail_main',
                                               template_name='core/detail.html', key='name', from_params=False))

core.add_url_rule(rule='/api/products/', view_func=MainPageView.as_view('products',
                                                template_name='core/objects/products.html'))

core.add_url_rule(rule='/api/detail-product/', view_func=DetailProductView.as_view('detail',
                                                template_name='core/objects/detail_modal.html', key='id'))
