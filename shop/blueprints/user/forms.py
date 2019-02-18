from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from .models import UserModel

class MainLoginForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])



class LoginForm(MainLoginForm):
    login_model = UserModel

    submit = SubmitField('Login')


    def validate_password(self, field):
        user = self.login_model.query.filter_by(name=self.data['name']).first()
        if not user or not user.check_password(field.data):
            raise ValidationError('Password or username incorrect')
        self.login_user_instance = user



class RegisterForm(MainLoginForm):

    password2 = PasswordField(validators=[EqualTo('password'), DataRequired()])
    email = StringField('Email', validators=[Email()])




