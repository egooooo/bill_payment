from flask import request
from flask_restful import Resource

from app import api, db, models


class PaymentApi(Resource):
    def post(self):

        return {"result": 200}, 200


api.add_resource(PaymentApi, '/')
