import os
import json
import requests

from flask import request, jsonify, make_response
from flask_restful import Resource
from hashlib import sha256

from app import api, db
from app.models import Payment, PaymentLog

from config import CURRENCY, CURRENCY_CODE, SHOP_ID, SECRET_KEY, PAYWAY, \
    URL_EN_PAY, URL_BILL_CRATE, URL_INVOICE_CRATE, \
    EUR_PARAMS, USD_PARAMS, RUB_PARAMS

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

    # logging.info(f'pay_log_save:\npayment_id: {payment_id}\n'
    #              f'send_data: {send_data}\nresponse: {response}')


def make_sign(params, data):
    sing = ':'.join([data.get(p) for p in sorted(params)]) + SECRET_KEY
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

        # Required data set for sending
        send_data = dict()

        if pay.pay_currency == 'EUR':
            send_data['amount'] = str(pay.pay_amount)
            send_data['currency'] = str(CURRENCY_CODE.get(pay.pay_currency))
            send_data['description'] = pay.description
            send_data['shop_id'] = str(SHOP_ID)
            send_data['shop_order_id'] = str(pay.id)
            send_data['sign'] = make_sign(EUR_PARAMS, send_data)
            send_data['url'] = URL_EN_PAY

            # logging.info(f'EUR -- Send_data: {send_data}')

            # Save logs
            pay_log_save(pay.id, json.dumps(send_data))

            response = jsonify(send_data)
            response.headers.set('Access-Control-Allow-Origin', '*')
            return make_response(response, 200)

        if pay.pay_currency == 'USD':
            send_data['payer_currency'] = str(CURRENCY_CODE.get(pay.pay_currency))
            send_data['shop_amount'] = str(pay.pay_amount)
            send_data['shop_currency'] = str(pay.pay_amount)
            send_data['shop_id'] = str(SHOP_ID)
            send_data['shop_order_id'] = str(pay.id)
            send_data['sign'] = make_sign(USD_PARAMS, send_data)

            # logging.info(f'USD -- send data: {send_data}')
            try:
                response_data = requests.post(
                    URL_BILL_CRATE,
                    json=send_data,
                    headers={'Content-Type': 'application/json'}
                )
            except:
                return make_response(jsonify({"error": "BAD REQUEST"}), 400)

            resp = json.loads(response_data.content)

            if resp.get('result') is False:
                # logging.info(f'USD -- response result is False: {resp}')
                return make_response(jsonify({"error": resp}), 400)

            # logging.info(f'USD -- response: {resp}')

            # Save logs
            pay_log_save(pay.id, json.dumps(send_data), json.dumps(resp))
            response = jsonify({"url": resp.get('data').get('url')})
            response.headers.set('Access-Control-Allow-Origin', '*')
            return make_response(response, 200)

        if pay.pay_currency == 'RUB':
            send_data['amount'] = str(pay.pay_amount)
            send_data['currency'] = str(CURRENCY_CODE.get(pay.pay_currency))
            send_data['payway'] = PAYWAY
            send_data['shop_id'] = str(SHOP_ID)
            send_data['shop_order_id'] = str(pay.id)
            send_data['sign'] = make_sign(RUB_PARAMS, send_data)

            # logging.info(f'RUB -- send data: {send_data}')

            try:
                response_data = requests.post(
                    URL_INVOICE_CRATE,
                    json=send_data,
                    headers={'Content-Type': 'application/json'}
                )
            except:
                return make_response(jsonify({"error": "BAD REQUEST"}), 400)

            resp = json.loads(response_data.content)

            if resp.get('result') is False:
                # logging.info(f'USD -- response result is False: {resp}')
                return make_response(jsonify({"error": resp}), 400)

            # logging.info(f'EUR -- Send_data: {send_data}')
            pay_log_save(pay.id, json.dumps(send_data), json.dumps(resp))

            response = jsonify(
                {
                    "method": resp.get('data').get('method'),
                    "url": resp.get('data').get('url')
                }
            )
            response.headers.set('Access-Control-Allow-Origin', '*')
            return make_response(response, 200)


api.add_resource(PaymentApi, '/')
