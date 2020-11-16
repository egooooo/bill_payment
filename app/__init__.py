import os

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

import config
import logging


# Logger
logging.basicConfig(
    filename=f'{os.path.dirname(os.path.realpath(__file__))}/../logs/log.log',
    level=logging.INFO
)


app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

from app import routes, service, view
