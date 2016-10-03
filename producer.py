import zmq
import json
import miniqservice
from threading import Thread
import sys

commandSocket = miniqservice.connectCommandServer("127.0.0.1")
miniqservice.createQueue(commandSocket,"STZ")
miniqservice.createDb(commandSocket)
miniqservice.startProducer(commandSocket)

class ProducerThread(Thread):

    def __init__(self,msg):
        Thread.__init__(self)
        self.msg = msg

    def run(self):
        producerSocket = miniqservice.producerConnect("127.0.0.1")
        ack = miniqservice.producerSend(producerSocket,self.msg)

if __name__ == '__main__':

    threads = []
    for i in range(0,4):
        msg = "producer" + str(i)
        producer = ProducerThread(msg)
        producer.start()
        threads.append(producer)

    for t in threads:
        t.join()
