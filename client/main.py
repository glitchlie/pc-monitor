from client import Client
from monitor import Monitor
from time import sleep


def getLocation(self):
    return os.path.dirname(os.path.realpath(__file__))


def loadConfig(self, path):
    import yaml

    path = os.path.join(path, "config.yaml")
    with open(path, 'r') as cfg:
        return yaml.safe_load(cfg)


if __name__ == "__main__":
    mon = Monitor()
    cli = Client()
    if cli.connectToServer():
        while True:
            stats = mon.getAllStats()
            cli.sendMessage(stats)
            sleep(1)
