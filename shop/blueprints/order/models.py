from flask import url_for

from app import db
from blueprints.core.model_mixins import BaseShopMixin


from datetime import datetime

class Shipping(BaseShopMixin):
    name = db.Column(db.String(124), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    contact = db.Column(db.String(66))
    active = db.Column(db.Boolean, default=True)
    orders = db.relationship('OrderModel', backref='shipping', lazy='dynamic')

    def __str__(self):
        return self.name


class OrderModel(BaseShopMixin):


    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    address = db.Column(db.String(200))
    country = db.Column(db.String(64))
    city = db.Column(db.String(64))
    postal_code = db.Column(db.String(64))
    paid = db.Column(db.Boolean, default=False)
    total_price = db.Column(db.Integer, default=0)
    email = db.Column(db.String(124))
    taxes = db.Column(db.Integer, default=0)
    shipping_id = db.Column(db.Integer,db.ForeignKey('shipping.id'))

    orderitems = db.relationship('OrderItem', backref='order', lazy='dynamic', passive_deletes=True)

    def make_sales(self):
        for item in self.orderitems:
            item.variant_product.sales += item.count
            item.variant_product.count -= item.count
            item.variant_product.last_sale = datetime.utcnow()
        self.paid = True
        self.save()


    def set_ship_price(self):
        self.total_price += self.shipping.price


    def set_taxes_price(self):
        # compute taxes
        self.total_price += self.taxes

    def get_full_address(self):
        return '%s, %s, %s, %s' % (self.country, self.city, self.address, self.postal_code)

    def set_items(self, cart):
        for variant, count, exceed in cart.get_items():
            if not exceed:
                price = variant.price * count
                OrderItem(count=count, variant_product=variant, price=price, order=self)
                self.total_price += price
        self.set_ship_price()
        self.set_taxes_price()
        self.save()



    def get_absolute_url(self):
        return url_for('order:order-pay-page')

    def __str__(self):
        return "Заказ № %d" % self.id

class OrderItem(BaseShopMixin):
    count = db.Column(db.Integer, default=1)
    price = db.Column(db.Integer, nullable=False)

    variant_product_id = db.Column(db.Integer, db.ForeignKey('variant.id', ondelete='RESTRICT'), nullable=False)
    variant_product = db.relationship('Variant')

    order_id = db.Column(db.Integer, db.ForeignKey(OrderModel.id,  ondelete='CASCADE'))


    def __str__(self):
        return str(self.id)

    def get_full_address(self):
        return '%s, %s, %s' % (self.order.country, self.order.city, self.order.address)

    @property
    def type_product(self):
        return self.variant_product.product

