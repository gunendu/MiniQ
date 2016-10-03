import zmq

def producerConnect(host):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://{}:5555'.format(host))
    return socket

def producerSend(socket,message):
    for i in range(6):
        socket.send(message)
        msgId = socket.recv()
        print "consumer ack",msgId

def createQueue(socket,name):
    msg = {}
    msg['type'] = "CREATE_QUEUE"
    msg['payload'] = {"name":name}
    socket.send(str(msg))

def createDb(socket):
    msg = {}
    msg['type'] = "CREATE_DB"
    msg['payload'] = {}
    socket.send(str(msg))

def startProducer(socket):
    msg = {}
    msg['type'] = "PRODUCE_MSG"
    msg['payload'] = {}
    socket.send(str(msg))

def consumerConnect(host,port_sub):
    context = zmq.Context()
    socket_sub = context.socket(zmq.REQ)
    socket_sub.connect ("tcp://localhost:%s" % port_sub)
    return socket_sub

def connectCommandServer(host):
    context = zmq.Context()
    socket_sub = context.socket(zmq.PAIR)
    socket_sub.connect('tcp://{}:5557'.format(host))
    return socket_sub

def startConsumer(socket):
    msg = {}
    msg['type'] = "CONSUME"
    msg['payload'] = {}
    socket.send(str(msg))

def notifyMinq(socket,msgId):
    socket.send(msgId)
