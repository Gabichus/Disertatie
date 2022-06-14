from flask import request
from flask_restful import Resource
from app.services.vm import powerOff, getListVM

class powerOffVM(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if json_data["vmName"] in getListVM() and json_data["vmName"] is not None:
            try:
                powerOff(json_data["vmName"])
                return {},200
            except:
                return {},500
        else:
            return {"error":"vm does not exist \
                 or vm name is empty"}, 400
