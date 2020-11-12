import pathlib
import os

BASE_DIR = pathlib.Path(__file__).parent

# currency_code
EUR = 978
USD = 840
RUB = 643

# Parameters for making queries
SHOP_ID = 5
SECRET_KEY = 'SecretKey01'
PAYWAY = 'payeer_rub'

# Urls
URL_PIASTRIX_EN = 'https://pay.piastrix.com/en/pay'
URL_PIASTRIX_BILL_CRATE = 'https://core.piastrix.com/bill/create'
URL_PIASTRIX_INVOICE_CRATE = 'https://core.piastrix.com/invoice/create'


class Config:
    DEBUG = True
    FLASK_ENV = 'development'
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///' + str(BASE_DIR / 'db.sqlite3'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '(8dvwf@-b62qg(q2xold%yr4%bz-gw9@anm5w39+id_rid2ntg'

