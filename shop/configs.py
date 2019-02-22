import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(BASE_DIR, os.environ.get('ENV_FILE') or 'flask.env'))


################################### DB
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://%s:%s@localhost/flask_shop' % (DB_USER, DB_PASSWORD)
SQLALCHEMY_TRACK_MODIFICATIONS = False
###############################

DEBUG = True

SECRET_KEY = os.environ.get('SECRET_KEY')


################# cart ###################

CART_SESSION_KEY = '_orders'
MAX_CART_SIZE = 100
ORDER_SESSION_ID = '_order'

################# admin #################################

FLASK_ADMIN_SWATCH = 'cerulean'

MEDIA_URL = '/media/'
MEDIA_PATH = '/home/borisov/flask_shop/app/staticfiles/media/'


################ pay
DEFAULT_CURRENCY =  'USD'
DEFAULT_CURRENCY_LABEL =  '$'

STRIPE_SERCRET_KEY =  os.environ['STRIPE_SECRET_KEY']
STRIPE_PUBLISHABLE_KEY =  os.environ['STRIPE_PUBLISHABLE_KEY']


############ static

COLLECT_STATIC_ROOT = '/home/borisov/flask_shop/app/staticfiles/static'