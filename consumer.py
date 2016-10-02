import zmq
import json
import miniqservice

producerSocket = miniqservice.producerConnect("127.0.0.1")

ack = miniqservice.producerSend(producerSocket,"Droplet Test!")

print "message ack",ack

consumerSocket = miniqservice.consumerConnect("127.0.0.1")

while True:
    msg = miniqservice.consumerReceive(consumerSocket)
    print "Message Received",msg
    miniqservice.notifyMinq(consumerSocket,msg['msgId'])
