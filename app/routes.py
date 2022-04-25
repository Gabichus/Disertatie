from app import api
from app.resources.export import exportVM
from app.resources.vm import VM
from app.resources.clone import cloneVM
from app.resources.importVM import importVM
from app.resources.powerOn import powerOnVM
from app.resources.powerOff import powerOffVM
# from app.resources.progress import progressVM

api.add_resource(VM,"/VM")
api.add_resource(exportVM,"/exportVM")
api.add_resource(importVM,"/importVM")
api.add_resource(cloneVM,"/cloneVM")
api.add_resource(powerOnVM,"/powerOnVM")
api.add_resource(powerOffVM,"/powerOffVM")
# api.add_resource(progressVM,"/progressVM")