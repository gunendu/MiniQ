import zmq
import app

def consumer():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://127.0.0.1:5556')
    while True:
        msg = socket.recv()
        print "consumer received message",msg
        socket.send("ack from consumer")

consumer()
