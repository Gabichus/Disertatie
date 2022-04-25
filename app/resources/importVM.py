from app import app
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from app.services.vm import powerOff, getListVM, importVM as importVMSerivce
from app.config import Config


class importVM(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        importVMSerivce(json_data)
