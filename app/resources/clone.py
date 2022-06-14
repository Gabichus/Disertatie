from flask import request
from flask_restful import Resource
from app.services.vm import getListVM, clone

class cloneVM(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if json_data["vmName"] in getListVM() and json_data["vmName"] is not None:
           try:
               clone(json_data)
               return {},201
           except:
               return {},500
        else:
            return {"error":"vm does not exist \
                 or vm name is empty"}, 400

        
