from flask import Flask,request,jsonify
import json
import datetime
import threading
import zmq
import leveldb
from random import randint
from datetime import datetime
import json
from Queue import Queue
import threading

queue = Queue(1000)
db = None
app = Flask(__name__)

def runBroker():
    global db
    db = leveldb.LevelDB("./db", create_if_missing=True)
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://127.0.0.1:5555')
    while True:
        msg = socket.recv()
        print "received Message",msg
        if "ack" in msg:
            socket.send("ack")
            t = threading.Thread(target=deleteMessage(msg))
            t.start()
        else:
            msgId = randint(0,1000)
            msgObj = {}
            msgObj['msgId'] = msgId
            msgObj['message'] = msg
            queue.put(msgObj)
            db.Put(str(msgId),json.dumps(msgObj))
            socket.send(str(msgId))

def deleteMessage(msgId):
    msg = json.loads(db.Get(str(msgId.split("_")[1])))
    db.Delete(str(msg['msgId']))

'''def produceMsg(msg):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    msgId = randint(0,1000)
    msgObj = {}
    msgObj['msgId'] = msgId
    msgObj['message'] = msg
    queue.put(msgObj)
    #db.Put(str(msgId),json.dumps(msgObj))
    print "qsuoze",queue.qsize()
    socket.send(str(msgId))'''

def consumeMsg():
    print 'consumeMsg is called'
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://127.0.0.1:5555')
    while True:
        msgObj = queue.get()
        queue.task_done()
        print "Consumer Mesage",msgObj
        socket.send("ack" +"_"+ str(msgObj['msgId']))
        msg = socket.recv()
        print "received reverse ack",msg

if __name__ == "__main__":
    t = threading.Thread(target=consumeMsg)
    t.start()
    runBroker()
