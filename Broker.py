import argparse
import zmq
import leveldb
from random import randint
from datetime import datetime
import json
from threading import Thread
from Queue import Queue

context = zmq.Context()
socket = context.socket(zmq.REP)
db = None
queue = Queue(1000)

def createBroker():
    socket.bind('tcp://127.0.0.1:5556')
    global db
    db = leveldb.LevelDB("./db", create_if_missing=True)

def produceMsg():
    global queue
    while True:
        msg = socket.recv()
        msgId = randint(0,1000)
        msgObj = {}
        msgObj['msgId'] = msgId
        msgObj['message'] = msg
        queue.put(msgObj)
        db.Put(str(msgId),json.dumps(msgObj))
        socket.send(str(msgId))

def consumeMsg():
    global queue
    while True:
        msgObj = queue.get()
        queue.task_done()
        socket.send(str(msgObj['msgId']))


createBroker()
produceMsg()
