from flask import Blueprint

from flask_restplus import Api, Namespace

blueprint = Blueprint(
    'Scheduling and listing jobs through aps scheduler Service', __name__)

api = Api(
    blueprint,
    default='scheduler',
    title='Scheduling and listing jobs through aps scheduler',
    description='Scheduling and listing jobs through aps scheduler',
    version='v1',
    doc='/doc/'
)

ns = Namespace('v1',
               description='Scheduling and listing jobs through aps scheduler',
               path='/')

api.add_namespace(ns)

# needed to register APIs in swagger
from scheduler.apis.v1 import routes
