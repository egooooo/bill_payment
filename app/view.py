from flask import request, jsonify, make_response
from flask_restful import Resource

from app import db
from app.models import Payment
from app.service import pay_log_save, make_sign, sender

from config import CURRENCY, CURRENCY_CODE, SHOP_ID, PAYWAY, \
    URL_EN_PAY, URL_BILL_CRATE, URL_INVOICE_CRATE, EUR_PARAMS, USD_PARAMS, \
    RUB_PARAMS

import json
import logging


class PaymentApi(Resource):
    def post(self):
        data = json.loads(request.data)

        if data.get('pay_amount') is None:
            return make_response(
                jsonify({"error": {"message": "BAD REQUEST"}}), 400
            )

        if data.get('pay_currency') not in CURRENCY:
            return make_response(
                jsonify({"error": {"message": "BAD REQUEST"}}), 400
            )

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

            # Save logs
            pay_log_save(pay.id, json.dumps(send_data))
            logging.info(f'EUR -- send_data: {send_data}')

            return make_response(jsonify(send_data), 200)

        if pay.pay_currency == 'USD':
            send_data['payer_currency'] = str(CURRENCY_CODE.get(pay.pay_currency))
            send_data['shop_amount'] = str(pay.pay_amount)
            send_data['shop_currency'] = str(CURRENCY_CODE.get(pay.pay_currency))
            send_data['shop_id'] = str(SHOP_ID)
            send_data['shop_order_id'] = str(pay.id)
            send_data['sign'] = make_sign(USD_PARAMS, send_data)

            # send data
            resp = sender(send_data, URL_BILL_CRATE)
            logging.info(f'USD -- sender: {send_data}')

            # Save logs
            pay_log_save(pay.id, json.dumps(send_data), json.dumps(resp))
            logging.info(f'USD -- send_data: {send_data}')

            if resp.get('error'):
                return make_response(resp)

            return make_response(jsonify({"url": resp.get('url')}), 200)

        if pay.pay_currency == 'RUB':
            send_data['amount'] = str(pay.pay_amount)
            send_data['currency'] = str(CURRENCY_CODE.get(pay.pay_currency))
            send_data['payway'] = PAYWAY
            send_data['shop_id'] = str(SHOP_ID)
            send_data['shop_order_id'] = str(pay.id)
            send_data['sign'] = make_sign(RUB_PARAMS, send_data)

            # send data
            resp = sender(send_data, URL_INVOICE_CRATE)
            logging.info(f'RUB -- sender: {send_data}')

            # save logs
            pay_log_save(pay.id, json.dumps(send_data), json.dumps(resp))
            logging.info(f'RUB -- send_data: {send_data}')

            if resp.get('error'):
                return make_response(resp)

            response = jsonify(
                {
                    "data": resp.get('data'),
                    "method": resp.get('method'),
                    "url": resp.get('url')
                }
            )
            return make_response(response, 200)
