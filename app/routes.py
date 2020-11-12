import os
import json

from flask import request
from flask_restful import Resource
from hashlib import sha256

from app import api, db
from app.models import Payment

from config import CURRENCY, EUR, USD, RUB, SHOP_ID, SECRET_KEY, PAYWAY, \
    URL_PIASTRIX_EN_PAY, URL_PIASTRIX_BILL_CRATE, URL_PIASTRIX_INVOICE_CRATE, \
    KEYS_SORTED

# import logging
#
#
# # Logger
# logging.basicConfig(
#     filename=f'{os.path.dirname(os.path.realpath(__file__))}/../logs/log.log',
#     level=logging.INFO
# )


def make_sign(keys, data):
    sing = ':'.join([data.get(key) for key in sorted(keys)]) + SECRET_KEY
    return sha256(sing.encode()).hexdigest()


class PaymentApi(Resource):
    def post(self):
        data = json.loads(request.data)

        if data.get('pay_currency') not in CURRENCY:
            return f'BAD REQUEST', 400

        pay = Payment(
            pay_amount=data.get('pay_amount'),
            pay_currency=data.get('pay_currency'),
            description=data.get('description')
        )
        db.session.add(pay)
        db.session.commit()

        if pay.pay_currency == 'EUR':
            send_data = {
                'amount': str(pay.pay_amount),
                'currency': str(EUR),
                'description': pay.description,
                'shop_id': str(SHOP_ID),
                'shop_order_id': str(pay.id),
            }

            send_data.update(
                {
                    'sign': make_sign(KEYS_SORTED, send_data),
                    'url': URL_PIASTRIX_EN_PAY
                }
            )
            # logging.info(f'EUR. Send_data: {send_data}')

            return send_data, 200

        if pay.pay_currency == 'USD':
            pass

        if pay.pay_currency == 'RUB':
            pass

        return {"result": 200}, 200


api.add_resource(PaymentApi, '/')
