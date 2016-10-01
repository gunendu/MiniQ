import zmq
import app

def publishMsg():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://127.0.0.1:5555')
    i = 0
    while(i<10):
        socket.send("test")
        msg = socket.recv()
        i = i + 1

publishMsg()
