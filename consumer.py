import zmq
import json
import miniqservice
from threading import Thread
import sys

commandSocket = miniqservice.connectCommandServer("127.0.0.1")
miniqservice.startConsumer(commandSocket)

class ConsumerThread(Thread):

    def __init__(self,host,port_sub):
        Thread.__init__(self)
        self.host = host
        self.port_sub = port_sub

    def run(self):
        socket_sub = miniqservice.consumerConnect(self.host,self.port_sub)
        while True:
            socket_sub.send("pop a message from queue")
            string = socket_sub.recv()
            string = eval(string)
            print string['msgId']
            message = {}
            message['type'] = "DELETE_MSG"
            message['payload'] = string
            commandSocket.send(str(message))

if __name__ == '__main__':

    cthreads = []

    for i in range(0,3):
        consumer = ConsumerThread("127.0.0.1","5556")
        consumer.start()
        cthreads.append(consumer)

    for c in cthreads:
        c.join()
