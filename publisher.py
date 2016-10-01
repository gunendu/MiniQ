import zmq
import app

def publishMsg():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://127.0.0.1:5555')
    print "Published message"
    socket.send("test")
    msg = socket.recv()
    print "received ack",msg

publishMsg()
