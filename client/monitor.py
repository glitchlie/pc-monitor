import os
from time import time


class Monitor:
    def __init__(self):
        self.handle = self.loadDriver(self.getLocation())
        self.config = self.loadConfig(self.getLocation())


    def getLocation(self):
        return os.path.dirname(os.path.realpath(__file__))


    def loadConfig(self, path):
        import yaml

        path = os.path.join(path, "config.yaml")
        with open(path, 'r') as cfg:
            return yaml.safe_load(cfg)


    def loadDriver(self, path):
        import clr

        path = os.path.join(path, "drivers", "OpenHardwareMonitorLib")
        clr.AddReference(path)
        from OpenHardwareMonitor import Hardware

        handle = Hardware.Computer()
        handle.MainboardEnabled = True
        handle.CPUEnabled = True
        handle.RAMEnabled = True
        handle.GPUEnabled = True
        handle.HDDEnabled = True
        handle.Open()

        return handle


    def printAllSensors(self):
        for h in self.handle.Hardware:
            h.Update()
            for sensor in h.Sensors:
                print("---------------")
                print(sensor.Identifier)
                print(sensor.Name + ' ' + str(sensor.Value))


    def getGPUStats(self):
        stats = dict()
        for h in self.handle.Hardware:
            h.Update()
            for sensor in h.Sensors:
                if (u"GPU" in sensor.Name) and (u"temperature" in str(sensor.Identifier)):
                    stats["core_temperature"] = sensor.Value
                elif (u"GPU" in sensor.Name) and (u"clock/0" in str(sensor.Identifier)):
                    stats["core_clock"] = sensor.Value
                elif (u"GPU" in sensor.Name) and (u"fan/0" in str(sensor.Identifier)):
                    stats["fan_rpm"] = sensor.Value
                elif (u"GPU" in sensor.Name) and (u"load/0" in str(sensor.Identifier)):
                    stats["core_load"] = sensor.Value
                elif u"GPU" in sensor.Name:
                    sensor_name = sensor.Name.split(' ', 1)[-1]
                    sensor_name = sensor_name.lower().replace(' ', '_')
                    stats[sensor_name] = sensor.Value

        stats["client_name"] = self.config["client"]["name"]
        stats["scan_timestamp"] = int(time())

        return stats


    def getAllStats(self):
        stats = dict()
        stats["data"] = dict()
        stats["data"]["GPU"] = dict()
        stats["data"]["CPU"] = dict()
        stats["data"]["RAM"] = dict()
        stats["data"]["HDD"] = dict()

        for h in self.handle.Hardware:
            h.Update()
            for sensor in h.Sensors:
                # GPU
                if (u"GPU" in sensor.Name) and (u"temperature" in str(sensor.Identifier)):
                    stats["data"]["GPU"]["core_temperature"] = sensor.Value
                elif (u"GPU" in sensor.Name) and (u"clock/0" in str(sensor.Identifier)):
                    stats["data"]["GPU"]["core_clock"] = sensor.Value
                elif (u"GPU" in sensor.Name) and (u"fan/0" in str(sensor.Identifier)):
                    stats["data"]["GPU"]["fan_rpm"] = sensor.Value
                elif (u"GPU" in sensor.Name) and (u"load/0" in str(sensor.Identifier)):
                    stats["data"]["GPU"]["core_load"] = sensor.Value
                elif u"GPU" in sensor.Name:
                    sensor_name = sensor.Name.split(' ', 1)[-1]
                    sensor_name = sensor_name.lower().replace(' ', '_')
                    stats["data"]["GPU"][sensor_name] = sensor.Value
                # CPU
                elif u"CPU" in sensor.Name:
                    sensor_name = sensor.Name.split(' ', 1)[-1]
                    sensor_name = sensor_name.lower().replace(' ', '_')
                    stats["data"]["CPU"][sensor_name] = sensor.Value
                # RAM
                elif u"ram" in str(sensor.Identifier):
                    sensor_name = sensor.Name
                    sensor_name = sensor_name.lower().replace(' ', '_')
                    stats["data"]["RAM"][sensor_name] = sensor.Value
                # HDD
                elif u"hdd" in str(sensor.Identifier):
                    sensor_name = sensor.Name
                    sensor_name = sensor_name.lower().replace(' ', '_')
                    stats["data"]["HDD"][sensor_name] = sensor.Value

        stats["client_name"] = self.config["client"]["name"]
        stats["scan_timestamp"] = int(time())

        return stats
