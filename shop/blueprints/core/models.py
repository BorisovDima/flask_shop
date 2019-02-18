from flask import url_for

from .model_mixins import ShopMixin, BaseShopMixin, db

from datetime import datetime



class Category(ShopMixin):
     products = db.relationship('Product', backref='category', lazy='dynamic')

class Brand(ShopMixin):
    products = db.relationship('Product', backref='brand', lazy='dynamic')



class Variant(BaseShopMixin):

    size = db.Column(db.String(10))
    count = db.Column(db.Integer, default=1)
    sales = db.Column(db.Integer, default=0)
    price = db.Column(db.Integer, nullable=False)
    last_sale = db.Column(db.DateTime, default=datetime.utcnow)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'))

    def __str__(self):
        return '%s %s' % (self.product.name, self.size or '')

class Product(ShopMixin):


    features = db.Column(db.String(124))
    average_price = db.Column(db.Integer, nullable=False)

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    variants = db.relationship('Variant', backref='product', lazy='dynamic', passive_deletes=True)

    image1 = db.Column(db.Unicode(128))
    image2 = db.Column(db.Unicode(128))
    image3 = db.Column(db.Unicode(128))

    def get_count(self):
        return sum(v.count for v in self.variants)

    def get_size(self):
        return self.variants.filter(Variant.size!=None)

    def get_main_variant(self):
        return self.variants.first()

    def get_absolute_url(self):
        return url_for('core.detail_main', name=self.name)

    @property
    def image(self):
        for i in range(1,4):
            if getattr(self, 'image%s' % i, False):
                return getattr(self, 'image%s' % i)




