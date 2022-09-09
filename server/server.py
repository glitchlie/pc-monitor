from receiver import Receiver
from router import Router
from multiprocessing import Process
from threading import Thread


if __name__ == "__main__":
    recv = Receiver()
    rout = Router()
    recv_process = Thread(target=recv.mainLoop)
    rout_process = Thread(target=rout.consumeQueue, args=("clients_data", ))
    rout_process.start()
    recv_process.start()
