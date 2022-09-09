import pika
import json
from redis_client import Redis
from pprint import pprint


class Router:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        self.channel = self.connection.channel()
        self.redis_client = Redis()


    def consumeQueue(self, queue_name):
        try:
            self.channel.basic_consume(queue_name, on_message_callback=self.processMessage, auto_ack=True)
            self.channel.start_consuming()
        except pika.exceptions.ChannelClosedByBroker:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
            self.channel = self.connection.channel()
            
            print("[ERROR]: Seems that %s doesnt exists, declaring" % (queue_name))
            self.channel.queue_declare(queue=queue_name)
            
            print("[INFO]: Declared %s" % (queue_name))


    def processMessage(self, channel, method_frame, header_frame, body):
        try:
            data = json.loads(body.decode("utf-8"))
            for hardware in data["data"].keys():
                for indicator in data["data"][hardware].keys():
                    list_name = "%s_%s_%s" % (data["client_name"], hardware, indicator)
                    self.redis_client.add_record(list_name, 
                                                 data["scan_timestamp"],
                                                 data["data"][hardware][indicator])
        except:
            print("[ERROR]: Cannot parse:\n")
            pprint(body.decode("utf-8"))


