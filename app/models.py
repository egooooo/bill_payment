from datetime import datetime
from app import db



class AbstractBaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now)
    updated = db.Column(db.DateTime, default=datetime.now)


class Payment(AbstractBaseModel):
    __tablename__ = 'payments'

    pay_amount = db.Column(db.Integer)
    pay_currency = db.Column(db.String(13))
    description = db.Column(db.Text)

    def __repr__(self):
        return f'Payment ID - {self.id}, ' \
               f'pay_currency - {self.pay_currency}, ' \
               f'amount - {self.pay_amount}'


class PaymentLog(AbstractBaseModel):
    __tablename__ = 'payment_logs'

    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'))
    send_data = db.Column(db.Text, default=None)
    response = db.Column(db.Text, default=None)
