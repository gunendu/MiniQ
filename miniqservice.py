import zmq

def producerConnect(host):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://{}:5555'.format(host))
    return socket

def producerSend(socket,message):
    socket.send(message)
    msgId = socket.recv()
    return msgId

def consumerConnect(host):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://{}:5556'.format(host))
    return socket

def consumerReceive(socket):
    msg = socket.recv()
    msg = eval(msg)
    return msg

def notifyMinq(socket,msgId):
    socket.send(msgId)
