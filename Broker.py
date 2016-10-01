from flask import Flask,request,jsonify
import argparse
import zmq
import leveldb
from random import randint
from datetime import datetime
import json
from threading import Thread
from Queue import Queue

def runBroker():
    while True:
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        queue = Queue(1000)
        socket.bind('tcp://127.0.0.1:5555')
        db = leveldb.LevelDB("./db", create_if_missing=True)
        msg = socket.recv()
        print msg

def produceMsg(msg):
    global queue
    while True:
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

if __name__ == "__main__":
    Broker.runBroker()
