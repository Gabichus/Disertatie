import os
import virtualbox
from os import listdir
from os.path import isfile, join
from app import vbox, vbmanager, vbmanagerInstance
from app.config import Config

def createHardDisk(vmName,storageSize,storageType):

    disk = vbox.create_medium(format_p="vdi",
                             location=Config.vmPath+vmName+"\\"+vmName+".vdi",
                             access_mode= virtualbox.library.AccessMode.read_write,
                             a_device_type_type=virtualbox.library.DeviceType.hard_disk)

    disk.create_base_storage(storageSize*1024*1000000,[virtualbox.library.MediumVariant(Config.storageType.get(storageType))])

    return disk

def attachDisk(vmName,disk):
    vm = vbmanagerInstance.find_machine(vmName)
    session = virtualbox.Session()
    try:
        vm.lock_machine(session, virtualbox.library.LockType.write)
        session.machine.attach_device(name="SATA",
                          controller_port=0,
                          device=0,
                          type_p=virtualbox.library.DeviceType.hard_disk,
                          medium=disk)
        
    except Exception as e:
        print(e)
    finally:
        session.machine.save_settings()
        session.unlock_machine()


def createOpticalDisk(vmName,osImageName):
    os.system('VBoxManage storageattach {vmName} --storagectl "IDE" --port 0  --device 0 --type dvddrive --medium C:\\Users\\Gabichus\\Desktop\\Disertatie\\systems\\{osImageName}'.format(vmName=vmName,osImageName=osImageName))