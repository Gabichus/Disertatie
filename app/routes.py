from app import api
# from app.resources.export import exportVM
from app.resources.vm import VM
# from app.resources.clone import cloneVM

api.add_resource(VM,"/VM")
# api.add_resource(exportVM,"/exportVM")
# api.add_resource(cloneVM,"/cloneVM")