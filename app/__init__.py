import virtualbox
from flask import Flask
from flask_restful import Resource, Api

vbox = virtualbox.VirtualBox()
vbmanager = virtualbox.Manager()
vbmanagerInstance = vbmanager.get_virtualbox()
app = Flask(__name__)
api = Api(app)

from app import routes