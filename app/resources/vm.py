from app import app
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from app.services.vm import getOsList, getListVM, createVm as createVmSerivce, deleteVm, modifyVM
from app.config import Config

parser = reqparse.RequestParser()
parser.add_argument('vmName', type=str)
parser.add_argument('osType', type=str)
parser.add_argument('cpuCore', type=int)
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
        cpuCore = args['cpuCore']
        ram = args['ram']
        vRam = args['vRam']
        graphicsController = args['graphicsController']
        network = args['network']
        storageType = args['storageType']
        storageSize = args['storageSize']
        storageName = args['storageName']
        storageBootable = args['storageBootable']
        osImageName = args['osImageName']

        if vmName in getListVM() or vmName is None:
            return "vmName"

        if osType is None:
            return "osType"

        if cpuCore is None or cpuCore > Config.maxCpu:
            return "cpuCore"

        if ram is None or ram > Config.maxRam:
            return "ram"

        if vRam is None or vRam > Config.maxVRam:
            return "vram"

        if graphicsController and not Config.graphicsController.get(graphicsController):
            return "graphicsController"

        if not Config.networkAddapter.get(network):
            return "network"

        if storageType not in Config.storageType:
            return "storageType"

        if storageSize is None or storageSize > Config.maxStorage:
            return "storageSize"

        if storageName is None:
            return "storageName"

        if not isinstance(storageBootable,bool):
            return "storageBootable"

        if osImageName not in getOsList():
            return "osImageName"

        storageBootable = "on" if storageBootable else "off"
        
        createVmSerivce(vmName,osType,cpuCore,ram,vRam,graphicsController,network,storageType,storageSize,storageName,storageBootable,osImageName)

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

        

        
        
