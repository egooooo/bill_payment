from app import api
from app.view import PaymentApi


api.add_resource(PaymentApi, '/')
