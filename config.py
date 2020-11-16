import pathlib
import os

BASE_DIR = pathlib.Path(__file__).parent

# currency_code
CURRENCY_CODE = {
    "EUR": 978,
    "USD": 840,
    "RUB": 643
}

CURRENCY = ["EUR", "USD", "RUB"]

EUR_PARAMS = ['amount', 'currency', 'shop_id', 'shop_order_id']
USD_PARAMS = ['shop_amount', 'shop_currency', 'shop_id', 'shop_order_id',
              'payer_currency']
RUB_PARAMS = ['amount', 'currency', 'payway', 'shop_id', 'shop_order_id']

# Parameters for making queries
SHOP_ID = 5
SECRET_KEY = 'SecretKey01'
PAYWAY = 'advcash_rub'

# PIASTRIX URLS
URL_EN_PAY = 'https://pay.piastrix.com/en/pay'
URL_BILL_CRATE = 'https://core.piastrix.com/bill/create'
URL_INVOICE_CRATE = 'https://core.piastrix.com/invoice/create'


class Config:
    DEBUG = True
    FLASK_ENV = 'development'
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///' + str(BASE_DIR / 'db.sqlite3')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '(8dvwf@-b62qg(q2xold%yr4%bz-gw9@anm5w39+id_rid2ntg'
