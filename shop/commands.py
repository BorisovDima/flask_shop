import click
from flask.cli import AppGroup
from flask import current_app
from blueprints.user.models import UserModel
from blueprints.core.models import Product,  Variant, Brand, Category

class UserExist(Exception): pass
class PasswordsMismatch(Exception): pass


user_cli = AppGroup('create_user')

@user_cli.command('superuser')
@click.argument('name')
@click.argument('password')
@click.argument('password_2')
@click.argument('email', required=False)
def create_user(name, password, password_2, email=None):
    if password != password_2:
        raise PasswordsMismatch('Passwords Mismatch')
    if UserModel.query.filter_by(name=name).first():
        raise UserExist('User already exist')
    superuser = UserModel(name=name, is_staff=True, is_superuser=True, email=email)
    superuser.set_password(password)
    superuser.save()
    print('Superuser create!')

current_app.cli.add_command(user_cli)


product_cli = AppGroup('create_product')

@product_cli.command('test_products')
def create_products(count=50):
    for i in range(1, count):
        brand = Brand(name='Test brand %s' % i)
        category = Category(name='Test category %s' % i)
        image = 'media/shop_media/Freedom_Isnt_Free_357230623_thumb.jpg'
        a_p = sum(i*(n+1) for n in range(4)) // 4
        product = Product(image1=image, category=category, brand=brand, name='test product% s' % i, average_price=a_p)
        for n, j in enumerate(['L', 'M', 'XL', 'XXL']):
            price = i*(n+1)
            Variant(product=product, count=count, price=price, size=j)
        product.save()
        print('Product %s create!' % product.id)


current_app.cli.add_command(product_cli)