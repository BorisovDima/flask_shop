from flask import current_app


from blueprints.core.models import Variant



CART_SESSION_KEY = current_app.config['CART_SESSION_KEY']
MAX_CART_SIZE = current_app.config['MAX_CART_SIZE']

class CartObj:
    def __init__(self, session):
        self.session = session
        self.orders = session.setdefault(CART_SESSION_KEY, {})
        self.items = None


    def get_items(self):
        if not self.items:
            pk = [key for key, _ in self]
            self.items = Variant.query.filter(Variant.id.in_(pk))
        for p in self.items:
            yield p, self.orders[str(p.id)], self.exceed(p)

    def __iter__(self):
       yield from self.orders.items()

    def action(self, event, id):
        """type(id) == str"""
        self.session.modified = True
        self.session.permanent = True
        return getattr(self, '_'+event)(str(id))


    def _add(self, id):
        if self.orders.get(id):
            self.orders[id] += self.orders[id] < MAX_CART_SIZE
        else:
            self.orders[id] = 1

    def _delete(self, id):
        self.orders[id] -= self.orders[id] > 1

    def _delete_all(self, id):
        del self.orders[id]
        if self.items: self.items = self.items.filter(Variant.id!=id)

    def _clear(self, _):
        self.orders.clear()
        self.items = None

    def exceed(self, variant):
        return variant.count < self.orders[str(variant.id)]

    def count_order(self, id):
        return self.orders.get(str(id))

    @property
    def count(self):
        return sum((val for _, val in self))


    @property
    def total_price(self):
        return sum((float(obj.price)*count for obj, count, exceed in self.get_items() if not exceed))