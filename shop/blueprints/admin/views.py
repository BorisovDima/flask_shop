from app import db, admin
from wtforms import HiddenField
from flask_login import current_user
from flask import redirect, url_for

from blueprints.core.models import Product, Brand, Category, Variant
from blueprints.order.models import OrderModel, Shipping, OrderItem
from blueprints.user.models import UserModel

from .forms import MyImageUploadField, MakeSlug, VariantsInlineForm
from .mixins import MyAdminView



class ProductAdmin(MyAdminView):
    column_exclude_list = ('image1', 'image2', 'image3', 'features')
    inline_models = (VariantsInlineForm(Variant),)
    form_excluded_columns = ('variants')
    form_extra_fields = {'image%s' % i: MyImageUploadField() for i in range(1, 4)}
    form_extra_fields.update({'slug': HiddenField(validators=[MakeSlug()])})


class UserAdmin(MyAdminView):
    column_exclude_list = ('password', 'date_create')

    def is_accessible(self):
        return current_user.is_superuser

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.index'))


    def create_model(self, form):
        data = getattr(form, 'data')
        password = data.pop('password')
        del data['csrf_token']
        user = UserModel(**data)
        user.set_password(password)
        user.save()

    def update_model(self, form, model):
        pass


class BrandAdmin(MyAdminView): pass
class CategoryAdmin(MyAdminView): pass
class OrderAdmin(MyAdminView): pass
class ShippingAdmin(MyAdminView): pass
class VariantAdmin(MyAdminView): pass

admin.add_view(BrandAdmin(Brand, db.session, name='Brand'))
admin.add_view(CategoryAdmin(Category, db.session, name='Category'))
admin.add_view(OrderAdmin(OrderModel, db.session, name='Orders'))
admin.add_view(ShippingAdmin(Shipping, db.session, name='Shipping'))
admin.add_view(ProductAdmin(Product, db.session, name='Product'))
# admin.add_view(MyAdminView(OrderItem, db.session, name='Order items'))
admin.add_view(VariantAdmin(Variant, db.session, name='Variants'))
admin.add_view(UserAdmin(UserModel, db.session, name='Users'))







