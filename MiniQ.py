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
import threading

queue = Queue.Queue()
db = None

class MiniQ(threading.Thread):

    def __init__(self,q,host,port):
        self.q = q
        self.host = host
        self.port = port
        threading.Thread.__init__ (self)

    def run(self):
        global db
        db = leveldb.LevelDB("./db", create_if_missing=True)
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind('tcp://{}:{}'.format(self.host,self.port))
        while True:
            msg = socket.recv()
            msgId = str(randint(0,100000))
            msgObj = {}
            msgObj['msgId'] = msgId
            msgObj['message'] = msg
            self.q.put(msgObj)
            db.Put(msgId,json.dumps(msgObj))
            socket.send(msgId)

miniq = MiniQ(queue,'127.0.0.1','5555')
miniq.start()

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://127.0.0.1:5556')
while True:
    msgObj = queue.get()
    queue.task_done()
    socket.send_string(str(msgObj))
    msgId = socket.recv()
    print "ack consumer",msgId
    db.Delete(str(msgId))
