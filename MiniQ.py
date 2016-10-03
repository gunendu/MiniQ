import time
import json
import datetime
import threading
import zmq
import leveldb
from random import randint
from datetime import datetime
import json
import Queue
from threading import Thread
import sys

queue = None
db = None

def produceMessage(host,port):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://{}:{}'.format(host,port))
    while True:
        msg = socket.recv()
        print "got message",msg
        msgId = str(randint(0,100000))
        msgObj = {}
        msgObj['msgId'] = msgId
        msgObj['message'] = msg
        queue.put(msgObj)
        db.Put(msgId,json.dumps(msgObj))
        socket.send(msgId)

def consumeMessage():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://127.0.0.1:5556')
    topic = 9
    while True:
        msg = socket.recv()
        msgObj = queue.get()
        queue.task_done()
        socket.send(str(msgObj))

class commandServer(Thread):

    def __init__(self):
        Thread.__init__ (self)

    def run(self):
        global queue,db
        context = zmq.Context()
        socket = context.socket(zmq.PAIR)
        socket.bind('tcp://127.0.0.1:5557')
        topic = 10
        while True:
            msg = socket.recv()
            msg = eval(msg)
            if msg['type'] is "PRODUCE_MSG":
                p = threading.Thread(target=produceMessage,args=("127.0.0.1","5555"))
                p.start()

            if msg['type'] is "CONSUME":
                c = threading.Thread(target=consumeMessage)
                c.start()

            if msg['type'] is "DELETE_MSG":
                payload = msg['payload']
                db.Delete(payload['msgId'])

            if msg['type'] is "QUEUE_SIZE":
                size = queue.qsize()
                socket.send(str(size))

            if msg['type'] is "CREATE_QUEUE":
                queue = Queue.Queue()

            if msg['type'] is "CREATE_DB":
                db = leveldb.LevelDB("./db", create_if_missing=True)

            if msg['type'] is "RELOAD_MSGS":
                for key,val in db:
                    print key,val    

if __name__ == '__main__':

    cserver = commandServer()
    cserver.start()
    cserver.join()

    sys.exit()
    print "exit main"
