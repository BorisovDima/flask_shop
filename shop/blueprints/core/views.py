from .mixins import FilterView, WrapJsonMixin, DetailView
from .models import Product
from .filters import FilterProduct

class MainPageView(WrapJsonMixin, FilterView):
    model = Product
    paginate = 8
    filter_class = FilterProduct

    def make_json(self, init):
        return {'html': init}



class DetailProductView(WrapJsonMixin, DetailView):
    model = Product

    def make_json(self, init):
        return {'html': init}


