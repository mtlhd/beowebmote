from zeroconf import ServiceBrowser, Zeroconf
import threading
import time

def striptrailing(astring, trailing):
    thelen = len(trailing)
    if astring[-thelen:] == trailing:
        return astring[:-thelen]
    return astring

def thread_function(object):
    zeroconf = Zeroconf()
    browser = ServiceBrowser(zeroconf, object.servicename, object)
    try:
        while object.active:
            time.sleep(.1)
            pass
    finally:
        zeroconf.close()

class BeoremoteListener:
    def __init__(self):
        self.active = True
        self.devices = {}
        self.servicename = "_beoremote._tcp.local."
        self.worker_thread = threading.Thread(target=thread_function, args=(self,), daemon=True)
        self.worker_thread.start()

    def remove_service(self, zeroconf, type, name):
        devicename = striptrailing(name, "." + self.servicename)
        print(devicename, " disconnected")
        devicekey = devicename.lower()
        self.devices.pop(devicekey)

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        devicename = striptrailing(name, "." + self.servicename)
        print(devicename, " connected")
        devicekey = devicename.lower()
        self.devices[devicekey] = info.parsed_addresses(3)[0]

    def update_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        devicename = striptrailing(name, "." + self.servicename)
        print(devicename, " updated")
        devicekey = devicename.lower()
        self.devices.pop(devicekey)
        self.devices[devicekey] = info.parsed_addresses(3)[0]

    def get_devices(self):
        return self.devices

    def stop(self):
        self.active = False
