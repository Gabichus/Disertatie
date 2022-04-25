from app import app
from flask import session, request
from flask_restful import Api, Resource, reqparse, abort
from app.services.vm import powerOff, getListVM, clone
from app.config import Config

class progressVM(Resource):
    def get(self):
        vmName = request.args.get('vmName', type = str)
        return session.get(vmName)