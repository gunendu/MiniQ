import argparse
import zmq
import Broker

parser = argparse.ArgumentParser(description='zeromq server/client')
parser.add_argument('--bar')
args = parser.parse_args()

if args.bar:
    # client
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://127.0.0.1:5556'.format(host))
    socket.send(args.bar)
    msg = socket.recv()
    print msg
