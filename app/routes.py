import os
import json
import requests

from flask import request, jsonify, make_response
from flask_restful import Resource
from hashlib import sha256

from app import api, db
from app.models import Payment, PaymentLog

from config import CURRENCY, CURRENCY_CODE, SHOP_ID, SECRET_KEY, PAYWAY, \
    URL_PIASTRIX_EN_PAY, URL_PIASTRIX_BILL_CRATE, URL_PIASTRIX_INVOICE_CRATE, \
    EUR_KEYS_SORTED, USD_KEYS_SORTED, RUB_KEYS_SORTED

# import logging
#
#
# # Logger
# logging.basicConfig(
#     filename=f'{os.path.dirname(os.path.realpath(__file__))}/../logs/log.log',
#     level=logging.INFO
# )


def pay_log_save(payment_id, send_data, response=None):
    pay_log = PaymentLog(
        payment_id=payment_id,
        send_data=send_data,
        response=response
    )
    db.session.add(pay_log)
    db.session.commit()

    # logging.info(f"pay_log: ID - {pay_log.id}, "
    #              f"payment_id - {pay_log.payment_id}, "
    #              f"send_data: {pay_log.send_data}")


def make_sign(keys, data):
    sing = ':'.join([data.get(key) for key in sorted(keys)]) + SECRET_KEY
    return sha256(sing.encode()).hexdigest()


class PaymentApi(Resource):
    def post(self):
        data = json.loads(request.data)

        if data.get('pay_currency') not in CURRENCY:
            return make_response(jsonify({"error": "BAD REQUEST"}), 400)

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
                'currency': str(CURRENCY_CODE.get(pay.pay_currency)),
                'description': pay.description,
                'shop_id': str(SHOP_ID),
                'shop_order_id': str(pay.id),
            }

            send_data.update(
                {
                    'sign': make_sign(EUR_KEYS_SORTED, send_data),
                    'url': URL_PIASTRIX_EN_PAY
                }
            )
            pay_log_save(pay.id, json.dumps(send_data))
            # logging.info(f'EUR. Send_data: {send_data}')

            response = jsonify(send_data)
            response.headers.set('Access-Control-Allow-Origin', '*')

            return make_response(response, 200)

        if pay.pay_currency == 'USD':
            send_data = {
                "payer_currency": str(CURRENCY_CODE.get(pay.pay_currency)),
                "shop_amount": str(pay.pay_amount),
                "shop_currency": str(CURRENCY_CODE.get(pay.pay_currency)),
                "shop_id": str(SHOP_ID),
                "shop_order_id": str(pay.id),
            }
            print(f'send_data: {send_data}')

            send_data.update(
                {
                    'sign': make_sign(EUR_KEYS_SORTED, send_data)
                }
            )
            response_data = requests.post(
                URL_PIASTRIX_BILL_CRATE,
                json=send_data,
                headers={'Content-Type': 'application/json'}
            )
            if response_data is None:
                return make_response(jsonify({"error": "BAD REQUEST"}), 400)

            resp = json.loads(response_data.content)

            pay_log_save(pay.id, json.dumps(send_data), resp)

            response = jsonify({"url": resp.get('data', {}).get('url')})
            response.headers.set('Access-Control-Allow-Origin', '*')
            return make_response(response, 302)

        if pay.pay_currency == 'RUB':
            return make_response({"result": 200}, 200)


api.add_resource(PaymentApi, '/')
