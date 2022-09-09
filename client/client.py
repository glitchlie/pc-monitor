import socket
import json
import os


class Client:
    def __init__(self):
        self.config = self.loadConfig(self.getLocation())
        self.sentMessages = 0


    def getLocation(self):
        return os.path.dirname(os.path.realpath(__file__))


    def loadConfig(self, path):
        import yaml

        path = os.path.join(path, "config.yaml")
        with open(path, 'r') as cfg:
            return yaml.safe_load(cfg)


    def connectToServer(self):
        print("[INFO]: Connecting to %s:%s" % (self.config["connection"]["address"],
                                               self.config["connection"]["port"]))
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(1)
        self.client.settimeout(self.config["connection"]["timeout"])
        self.client.connect((self.config["connection"]["address"],
                             self.config["connection"]["port"]))
        data = {"client_name": self.config["client"]["name"]}
        bytes_data = json.dumps(data).encode("utf-8")

        self.client.sendall(bytes_data)
        try:
            data = self.client.recv(1024)
            message = json.loads(data.decode("utf-8"))
            if message["connected"] == "true":
                print("[INFO]: Connected to %s:%s" % (self.config["connection"]["address"],
                                                       self.config["connection"]["port"]))
                return True

        except socket.timeout:
            self.client.close()
            print("[ERROR]: Can't connect to %s:%s" % (self.config["connection"]["address"],
                                                       self.config["connection"]["port"]))
            return False


    def sendMessage(self, data):
        data["message_num"] = self.sentMessages
        message = json.dumps(data).encode("utf-8")
        self.client.sendall(message)
        self.sentMessages += 1
