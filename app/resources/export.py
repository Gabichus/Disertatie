from app import app
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from app.services.vm import getOsList, getListVM, export
from app.config import Config

class exportVM(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if json_data["vmName"] in getListVM() and json_data["vmName"] is not None:
           export(json_data["vmName"])
