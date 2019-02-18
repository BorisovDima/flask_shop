from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField
from .models import Product, Category, Brand

import operator
from functools import partial as p

#################### mixins

class FieldMixin:
    def __init__(self, label='', validators=None,  field_name=None, lookup_exp=None, default='', **kwargs):
        self.lookup_exp = lookup_exp
        self.field_name = field_name
        super().__init__(label, validators, default=default, **kwargs)

    def filter_field(self, q):
        return q.filter(self.lookup_exp(self.data))



############### fields

class MyStringField(FieldMixin, StringField):pass
class MyIntegerField(FieldMixin, IntegerField): pass

class MySelectField(FieldMixin, SelectField):

    def __init__(self, *args, empty_label='---', **kwargs):
        self.empty_label = empty_label
        super().__init__(*args, **kwargs)

    def iter_choices(self):
        yield ('', self.empty_label, True)
        yield from super().iter_choices()


class MyOrderingField(FieldMixin, SelectField):

    def filter_field(self, q):
        exp, _ = self.choices.get(self.data, (False, False))
        return q.order_by(exp()) if exp else q

    def iter_choices(self):
        for value, (_, label) in self.choices.items():
            yield (value, label, self.coerce(value) == self.data)



############### forms
class FilterForm(FlaskForm):
    model = None

    def make_filtering(self, filter_objs):
        for f in self._fields.values():
            if f.data:
                filter_objs = f.filter_field(filter_objs)
        return filter_objs

############################

class FilterProduct(FilterForm):
    model = Product

    CHOICES_ORDERING = {'1': (model.name.asc, "по алфавиту"),
                        '2': (model.average_price.asc, "дешевые сверху"),
                        '3': (model.average_price.desc, "дорогие сверху")}


    name = MyStringField(field_name='name', lookup_exp=p(model.name.contains))
    category = MySelectField(field_name='category', lookup_exp=p(operator.eq, model.category_id),
                             choices=[(str(i.id), i.name) for i in Category.query], empty_label='Category')
    brand = MySelectField(field_name='brand', lookup_exp=p(operator.eq, model.brand_id),
                          choices=[(str(i.id), i.name) for i in Brand.query], empty_label='Brand')

    average_price = MyIntegerField('Цена ниже', field_name='average_price',
                                   lookup_exp=p(operator.lt, model.average_price))

    ordering = MyOrderingField('Сортировать', lookup_exp=p(model.query.order_by), choices=CHOICES_ORDERING)