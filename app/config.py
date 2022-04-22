class Config(object):
    maxCpu = 4
    maxRam = 8000
    maxStorage = 10000
    maxVRam = 128
    graphicsController = {"null":0, "vboxvga": 1, "vmsvga": 2, "vboxsvga": 3}
    networkAddapterType = {
        "Null": 0,
        "Am79C970A": 1,
        "Am79C973": 2,
        "I82540EM": 3,
        "I82543GC": 4,
        "I82545EM": 5,
        "Virtio": 6,
        "Am79C960": 7,
        "Virtio_1_0": 8}
    networkAddapter={
        "null": 0,
        "nat": 1,
        "bridged": 2,
        "internal": 3,
        "hostonly": 4,
        "generic": 5,
        "natnetwork": 6,
        "cloud": 7
    }
    cloneOptions={
            "Link":1,
            "KeepAllMACs":2,
            "KeepNATMACs":3,
            "KeepDiskNames": 4,
            "KeepHwUUIDs": 5
    }
    storageType = ["standard","fixed"]