from app import app
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from app.services.vm import getOsList, getListVM, createVM as createVmSerivce, deleteVm, modifyVM
from app.config import Config

parser = reqparse.RequestParser()
parser.add_argument('vmName', type=str)
parser.add_argument('osType', type=str)
parser.add_argument('cpuCount', type=int)
parser.add_argument('ram', type=int)
parser.add_argument('vRam', type=int)
parser.add_argument('graphicsController', type=str)
parser.add_argument('network', type=str)
parser.add_argument('storageType', type=str)
parser.add_argument('storageSize', type=int)
parser.add_argument('storageName', type=str)
parser.add_argument('storageBootable', type=bool)
parser.add_argument('osImageName', type=str)

class VM(Resource):
    def post(self):

        json_data = request.get_json(force=True)
        args = parser.parse_args()

        vmName = args['vmName']
        osType = args['osType']
        cpuCount = args['cpuCount']
        ram = args['ram']
        vRam = args['vRam']
        graphicsController = args['graphicsController']
        network = args['network']
        storageType = args['storageType']
        storageSize = args['storageSize']
        storageBootable = args['storageBootable']
        osImageName = args['osImageName']

        if vmName in getListVM() or vmName is None:
            return "vmName"

        if osType is None:
            return "osType"

        if cpuCount is None or cpuCount > Config.maxCpu:
            return "cpuCount"

        if ram is None or ram > Config.maxRam:
            return "ram"

        if vRam is None or vRam > Config.maxVRam:
            return "vram"

        if graphicsController is None and Config.graphicsController.get(graphicsController) is None:
            return "graphicsController"

        if Config.networkAddapter.get(network) is None:
            return "network"

        if Config.storageType.get(storageType) is None:
            return "storageType"

        if storageSize is None or storageSize > Config.maxStorage:
            return "storageSize"

        if not isinstance(storageBootable,bool):
            return "storageBootable"

        if osImageName not in getOsList():
            return "osImageName"

        storageBootable = "on" if storageBootable else "off"

        createVmSerivce(json_data)
       # createVmSerivce(vmName,osType,cpuCore,ram,vRam,graphicsController,network,storageType,storageSize,storageName,storageBootable,osImageName)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('vmName', type=str)
        
        vmName = parser.parse_args()['vmName']

        if vmName in getListVM() or vmName is None:
            deleteVm(vmName)

    def patch(self):
        json_data = request.get_json(force=True)
        
        if json_data["vmName"] in getListVM() and json_data["vmName"] is not None:
            modifyVM(json_data)

        

        
        
