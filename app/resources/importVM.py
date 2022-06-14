from flask import request
from flask_restful import Resource
from app.services.vm import getExportedVM, getListVM, importVM as importVMSerivce

class importVM(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if json_data["vmName"] not in getListVM() and json_data["vmName"] is not None:
            print(getExportedVM())
            if json_data["vmName"]+".ova" in getExportedVM():
                try:
                    importVMSerivce(json_data)
                    return {},201
                except:
                    return {},500
            else:
                return {"error":json_data["vmName"]+".ova not found"}, 409
        else:
            return {"error":"vm already exist \
                 or vm name is empty"}, 400

