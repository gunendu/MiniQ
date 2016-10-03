MiniQ:-

MiniQ is a broker that receives messages from multiple produces and consumer polls miniq to consume those messages.

Miniq uses a Queue to store messages in memory, and LevelDB for persistence storage.

CommandServer Thread Miniq:-

Any communication with miniq is prossible only through tcp layer, miniq uses zmq messaging service to send and receive messages.

Miniq has a CommandServer that starts as soon as you start the broker, commandserver binds itself to port 5557 for incoming messages, message format for commandserver contains type of message and the payload of the message.

supported message types  : -  CREATE_QUEUE, QUEUE_SIZE, DELETE_MSG etc

 So any communication from outside world with minq is by sending a tcp message to commandserver.

Producer Thread Miniq:-

Miniq starts the producer thread when its command server receives a message PRODUCE_MSG from client producer, producer thread binds itself to port 5555, and listens for any incoming messages from client producer. When it receives any message, it generates a random id, forms the messages and enques the message to queue and also calls leveldb Put to persist the message. Every incoming message from producer will be acknowledged by broker. Producer thread in miniq use zmq REQ-RES  pattern, so every incoming request(REQ) from producer is acknowledged by response(RES), request response is paired.

Consumer Thread Miniq:-

Miniq starts consumer thread starts when its command server receives a message CONSUME from client consumer, consumer thread binds itself to port 5556, and again using zmq REQ-RES pattern, client consumer must ask minq server it wants to consume a message, once server receives a message, it pops a message from queue and sends it to client consumer. Client receives the message and after processing it fires DELETE_MSG to command server, command server deleted the message from persitence with key as messageid.


Miniq Service :-

Its a layer that sits between clients and miniq server, all external entities like producer client and consumer client should communicate it through this service layer.

Producer client :-

producer client connects to miniq, send command to create queue, generates messages and send it through zmq protocol. There can be n number of producers that send messages at the same time.
Consumer client:- 

consumer client connects to miniq, send request to consume mesage, process mesage and notifies miniq to delete message.

LevelDb:-

Leveldb is file based persistence database that stores the data as key value pair, miniq uses it for persistence, every messageobject has messageid and message, so messageId is the key and value is the actual message.

If broker goes down messages can be retreived if it is not ack by consumer by iterating it through the db.

Queue:-

miniq uses a single queue for multiple producers and consumers, but can be extended to support multiple queues.

Restlayer:-

http layer can be added to receive stats about the queue, http layer can use the minq service layer to send any command to minq command server.













