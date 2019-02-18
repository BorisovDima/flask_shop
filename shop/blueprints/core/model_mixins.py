from app import db

from datetime import datetime
import sys


class BaseShopMixin(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_create = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def _commit(self):
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            print(error, file=sys.stderr)

    def delete(self):
        db.session.delete(self)
        self._commit()

    def save(self):
        db.session.add(self)
        self._commit()

class ShopMixin(BaseShopMixin):
    __abstract__ = True

    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(244))
    slug = db.Column(db.String(122), unique=True)

    def __str__(self):
        return self.name

