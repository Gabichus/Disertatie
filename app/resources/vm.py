from flask import request
from flask_restful import Resource
from app.services.vm import getOsList, getListVM, createVM as createVmSerivce, deleteVm, modifyVM
from app.config import Config

class VM(Resource):
    def post(self):

        json_data = request.get_json(force=True)

        if json_data["vmName"] in getListVM() or json_data["vmName"] is None:
            return {"error":"vmName already exist"},400

        if json_data["osType"] is None:
            return {"error":"osType parameter missing"},400

        if json_data["cpuCount"] is None or json_data["cpuCount"] > Config.maxCpu:
            return {"error":"cpuCount parameter missing"},400

        if json_data["ram"] is None or json_data["ram"] > Config.maxRam:
            return {"error":"ram parameter missing or ram exceed limit"},400

        if json_data["vRam"] is None:
            return {"error":"vram parameter missing"},400

        if json_data["vRam"] > Config.maxVRam:
            return {"error":"vram exceed limit"},400

        if json_data["graphicsController"] is None:
            return {"error":"graphicsController parameter missing"},400

        if Config.graphicsController.get(json_data["graphicsController"]) is None:
            return {"error":"graphicsController type not found"},400

        if Config.networkAddapter.get(json_data["network"]) is None:
            return {"error":"network type not found"},400

        if Config.storageType.get(json_data["storageType"]) is None:
            return {"error":"storageType not found"},400

        if json_data["storageSize"] is None or json_data["storageSize"] > Config.maxStorage:
            return {"error":"storageSize exceed limit"},400

        if json_data["osImageName"] not in getOsList():
            return {"error":"osImageName not found"},400

        createVmSerivce(json_data)

    def delete(self):
        json_data = request.get_json(force=True)

        if json_data["vmName"] in getListVM() and json_data["vmName"] is not None:
           try:
               deleteVm(json_data["vmName"])
               return {},201
           except:
               return {},500
        else:
            return {"error":"vm does not exist \
                 or vm name is empty"}, 400

    def patch(self):
        json_data = request.get_json(force=True)
        if json_data["vmName"] in getListVM() and json_data["vmName"] is not None:
           try:
               modifyVM(json_data)  
               return {},201
           except:
               return {},500
        else:
            return {"error":"vm does not exist \
                 or vm name is empty"}, 400
