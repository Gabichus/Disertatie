from app import app
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from app.services.vm import getExportedVM, getListVM, export
from app.config import Config

class exportVM(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if json_data["vmName"] in getListVM() and json_data["vmName"] is not None:
            if json_data["vmName"] not in getExportedVM():
                try:
                    export(json_data)
                    return {},201
                except:
                    return {},500
            else:
                return {"error":"already exist"}, 409
        else:
            return {"error":"vm not found"}, 406
