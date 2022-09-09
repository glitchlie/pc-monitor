import socket
import json
import os
import threading
import pika


class Receiver:
    def __init__(self):
        self.config = self.loadConfig(self.getLocation())
        self.connectedClients = list()


    def getLocation(self):
        return os.path.dirname(os.path.realpath(__file__))


    def loadConfig(self, path):
        import yaml

        path = os.path.join(path, "config.yaml")
        with open(path, 'r') as cfg:
            return yaml.safe_load(cfg)


    def handleClient(self, client, address, rabbit_connection, rabbit_channel, client_name):
        received_messages = 0
        while True:
            try:
                data = client.recv(1024).decode()
                if not data:
                    print("[WARNING]: Connection from %s:%s was reset" % (address[0], address[1]))
                    rabbit_connection.close()
                    break
                
                rabbit_channel.basic_publish(exchange="",
                                             routing_key="clients_data",
                                             body=data)
           
            except socket.timeout:
                print("[WARNING]: Connection from %s:%s was reset due to timeout" % (address[0], address[1]))
                rabbit_connection.close()
                self.connectedClients.remove(client_name)
                break
            

    def mainLoop(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.config["server"]["address"], self.config["server"]["port"]))
        server.listen(1)
        print("[INFO]: Listening on %s:%s" % (self.config["server"]["address"],
                                              self.config["server"]["port"]))

        while True:
            client, address = server.accept()
            print("[INFO]: Accepted connection from %s:%s" % (address[0],
                                                              address[1]))
            client.setblocking(1)
            client.settimeout(self.config["server"]["connection-timeout"])
            print("[INFO]: Set timeout %s s for %s:%s" % (self.config["server"]["connection-timeout"],
                                                          address[0],
                                                          address[1]))
            
            data = client.recv(1024)
            message = json.loads(data.decode("utf-8"))
            if message["client_name"]:
                rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters(self.config["rabbitmq"]["address"]))
                rabbit_channel = rabbit_connection.channel()
                rabbit_channel.queue_declare(queue="clients_data")
                print("[INFO]: Opened RabbitMQ channel on %s" % (self.config["rabbitmq"]["address"], ))
            
                client_handler = threading.Thread(target=self.handleClient, args=(client, 
                                                                                  address, 
                                                                                  rabbit_connection,
                                                                                  rabbit_channel,
                                                                                  message["client_name"]))
                client_handler.start()
                
                response = {"connected": "true"}
                response_data = json.dumps(response).encode("utf-8")
                client.sendall(response_data)
                self.connectedClients.append(message["client_name"])


if __name__ == "__main__":
    r = Receiver()
    r.mainLoop()
