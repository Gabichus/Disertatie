import time
import uuid
import pickle
import virtualbox
from os import listdir
from flask import session
from os.path import isfile, join
from app import vbox, vbmanager, vbmanagerInstance
from app.config import Config
from app.services.disk import createHardDisk, attachDisk, createOpticalDisk

def getExportedVM():
    return [f for f in listdir(Config.exportPath) if isfile(join(Config.exportPath, f))]
    
def getOsList():
    return [f for f in listdir(Config.systemsPath) if isfile(join(Config.systemsPath, f))]

def getListVM():
    return [m.name for m in vbox.machines]

def createVM(json_data):
    uuidNumber = uuid.uuid1()
    name = json_data["vmName"]
    primary_group = ""
    groups = []
    basefolder = Config.vmPath
    create_flags = "UUID=%s" % uuidNumber
  
    settings_file = vbox.compose_machine_filename(name, primary_group, create_flags, basefolder)
    vm = vbox.create_machine(settings_file, name, groups, os_type_id=json_data["osType"],flags=create_flags)
    vm.cpu_count = json_data["cpuCount"]
    vm.memory_size = json_data["ram"]
    vm.graphics_adapter.vram_size = json_data["vRam"]
    vm.graphics_adapter.graphics_controller_type =  virtualbox.library.GraphicsControllerType(Config.graphicsController.get(json_data["graphicsController"]))
    vm.get_network_adapter(0).enabled
    vm.get_network_adapter(0).attachment_type = virtualbox.library.NetworkAttachmentType(Config.networkAddapter.get(json_data["network"]))
    vm.add_storage_controller("SATA", virtualbox.library.StorageBus.sata)
    vm.add_storage_controller("IDE", virtualbox.library.StorageBus.ide)
    vbox.register_machine(vm)

    disk = createHardDisk(vmName=json_data["vmName"],storageSize=json_data["storageSize"],storageType=json_data["storageType"])
    attachDisk(vmName=json_data["vmName"],disk=disk)
    createOpticalDisk(json_data["vmName"],json_data["osImageName"])
    

# def createVm(vmName,osType,cpuCore,ram,vRam,graphicsController,network,storageType,storageSize,storageName,storageBootable,osImageName):
#     os.system('vboxmanage createvm --name {vmName} --ostype {osType} --register --basefolder C:\\Users\\Gabichus\\Desktop\\Disertatie\\vm'.format(vmName=vmName, osType=osType))
#     os.system('vboxmanage modifyvm {vmName} --cpus {cpuCore} --memory {ram} --vram {vRam}'.format(vmName=vmName, cpuCore=cpuCore, ram=ram, vRam=vRam))
#     os.system('vboxmanage modifyvm {vmName} --graphicscontroller {graphicsController}'.format(vmName=vmName, graphicsController=graphicsController))
#     os.system('VBoxManage modifyvm {vmName} --nic1 {network}'.format(vmName=vmName, network=network))
#     os.system('vboxmanage createhd --filename C:\\Users\\Gabichus\\Desktop\\Disertatie\\vm\\{vmName}\\{storageName} --size {storageSize} --variant {storageType}'.format(vmName=vmName,storageName=storageName,storageSize=storageSize,storageType=storageType))
#     os.system('vboxmanage storagectl {vmName} --name "{storageName}" --add sata --bootable {sotrageBootable}'.format(vmName=vmName, storageName=storageName, sotrageBootable=storageBootable))
#     os.system('vboxmanage storageattach {vmName} --storagectl "{storageName}" --port 0 --device 0 --type hdd --medium C:\\Users\\Gabichus\\Desktop\\Disertatie\\vm\\{vmName}\\{storageName}.vdi'.format(vmName=vmName,storageName=storageName))
#     os.system('vboxmanage storagectl {vmName} --name "ide ctl" --add ide'.format(vmName=vmName))
#     os.system('VBoxManage storageattach {vmName} --storagectl "ide ctl" --port 0  --device 0 --type dvddrive --medium C:\\Users\\Gabichus\\Desktop\\Disertatie\\systems\\{osImageName}'.format(vmName=vmName,osImageName=osImageName))
#     os.system('vboxmanage modifyvm {vmName} --vrde on'.format(vmName=vmName))
    # time.sleep(2)
    # os.system('VBoxManage startvm {vmName} --type separate') #headless(hidden)/separete(gui)

def deleteVm(vmName, delete=True):
    vm = vbmanagerInstance.find_machine(vmName)
    if vm.state >= virtualbox.library.MachineState.running:
        session = virtualbox.Session()
        vm.lock_machine(session,virtualbox.library.LockType.shared)
        try:
            progress = session.console.power_down()
            progress.wait_for_completion(-1)
        except Exception:
            print("Error powering off machine", file=sys.stderr)
        session.unlock_machine()
        time.sleep(
            0.5
        )  # TODO figure out how to ensure session is really unlocked...

    if delete:
        option = virtualbox.library.CleanupMode.full
    else:
        option = virtualbox.library.CleanupMode.detach_all_return_none
    media = vm.unregister(option)

    if delete:
        progress = vm.delete_config(media)
        progress.wait_for_completion(-1)
    media = []

def export(json_data):
    vmName = json_data["vmName"]
    vm = vbmanagerInstance.find_machine(vmName)

    try:
        appliance = vbox.create_appliance()
        vm.export_to(appliance, vmName)
        progress = appliance.write('ovf-2.0', [virtualbox.library.ExportOptions.create_manifest], Config.exportPath+'{vmName}.ova'.format(vmName=vmName))
        # while(progress.percent < 20):
        #     time.sleep(3)
        #     session[vmName] = progress.percent
        # progress.cancel()
    except Exception as e:
        print(e)
    finally:
        progress.cancel()
    #progress.wait_for_completion(-1)
    
def importVM(json_data):
    appliance = vbox.create_appliance()
    appliance.read(Config.exportPath+json_data["vmName"]+".ova")
    appliance.import_machines()

def modifyVM(json_data):
    session = vbmanager.get_session()
    
    try:
        vm = vbmanagerInstance.find_machine(json_data["vmName"])
        vm.lock_machine(session,virtualbox.library.LockType.write)

        if json_data["cpuCore"] != None and json_data["cpuCore"] != "":
            session.machine.cpu_count = json_data["cpuCore"]

        if json_data["ram"] != None and json_data["ram"] != "":
            session.machine.memory_size = json_data["ram"]

        if json_data["vRam"] != None and json_data["vRam"] != "":
            session.machine.graphics_adapter.vram_size = json_data["vRam"]

        if json_data["graphicsController"] != None and json_data["graphicsController"] != "":
            session.machine.graphics_adapter.graphics_controller_type =  virtualbox.library.GraphicsControllerType(Config.graphicsController.get(json_data["graphicsController"]))

        if json_data["network"] != None and json_data["network"] != "": 
            session.machine.get_network_adapter(0).enabled
            session.machine.get_network_adapter(0).attachment_type = virtualbox.library.NetworkAttachmentType(Config.networkAddapter.get(json_data["network"]))
            session.machine.get_network_adapter(0)
    except Exception as e:
        print(e)
    finally:
        session.machine.save_settings()
        session.unlock_machine()
    
def clone(json_data):
    uuidNumber = uuid.uuid1()
    vm = vbmanagerInstance.find_machine(json_data["vmName"])

    name = json_data["vmNameClone"]
    groups = []
    primary_group = ""
    basefolder = Config.vmPath
    create_flags = "UUID=%s" % uuidNumber
    mode = virtualbox.library.CloneMode.all_states

    options = [Config.cloneOptions.get(json_data.get('cloneOptions'))]
    if None in options:
        options = [virtualbox.library.CloneOptions(4)]

    settings_file = vbox.compose_machine_filename(name, primary_group, create_flags, basefolder)
    vm_clone = vbox.create_machine(settings_file, name, groups, os_type_id="",flags=create_flags)
    progress = vm.clone_to(vm_clone, mode, options)
    progress.wait_for_completion(-1)
    vbox.register_machine(vm_clone)

def powerOn(vmName):
    vm = vbmanagerInstance.find_machine(vmName)
    if vm.state != virtualbox.library.MachineState.running:
        session = virtualbox.Session()
        try:
            vm = vbmanagerInstance.find_machine(vmName)
            environment_changes = []
            name = "gui"
            progress = vm.launch_vm_process(session, name,environment_changes)
            progress.wait_for_completion(-1)
        except Exception as e:
            print(e)
        finally:
            session.unlock_machine()

def powerOff(vmName):
    vm = vbmanagerInstance.find_machine(vmName)
    if vm.state >= virtualbox.library.MachineState.running:
        session = virtualbox.Session()
        vm.lock_machine(session,virtualbox.library.LockType.shared)
        try:
            progress = session.console.power_down()
            progress.wait_for_completion(-1)
        except Exception:
            print("Error powering off machine", file=sys.stderr)
        session.unlock_machine()