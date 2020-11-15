from hashlib import sha256

from app import db
from app.models import PaymentLog
from config import SECRET_KEY

import requests
import json
import logging


def pay_log_save(payment_id, send_data, response=None):
    pay_log = PaymentLog(
        payment_id=payment_id,
        send_data=send_data,
        response=response
    )
    db.session.add(pay_log)
    db.session.commit()

    logging.info(f'pay_log_save:\npayment_id: {payment_id}\n'
                 f'send_data: {send_data}\nresponse: {response}')


def make_sign(params, data):
    sing = ':'.join([data.get(p) for p in sorted(params)]) + SECRET_KEY
    return sha256(sing.encode()).hexdigest()


def sender(data, url):
    try:
        response_data = requests.post(
            url,
            json=data,
            headers={'Content-Type': 'application/json'}
        )
    except:
        return {"error": {"message": "error while sending request"}}

    response = json.loads(response_data.content)

    if response.get('result') is False:
        return {"error": response}

    return response.get('data')
