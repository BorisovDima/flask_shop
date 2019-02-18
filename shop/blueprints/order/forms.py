from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Email, DataRequired
from .models import Shipping


class OrderForm(FlaskForm):

    first_name = StringField('First name',validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    postal_code = StringField('Postal code', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    shipping = RadioField('Shipping', choices=[(str(s.id), s.name) for s in Shipping.query.all()])

    make_order = SubmitField('Make order')

    def validate_shipping(self, field):
        if not field.data.isdigit(): raise ValidationError
        v = Shipping.query.get(field.data)
        if v is None: raise ValidationError
        field.data = v

    def get_order_data(self):
        return dict((k, v) for k, v in self.data.items() if k not in ['csrf_token', 'make_order'])






