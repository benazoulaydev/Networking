# MESSENGER TALK GROUP IN UDP

This Work enable to talk between multiple clients
via UDP connection. They can connect to a group, send messages, change their name in the group, left. This is a Single-Threaded connection, so only, so delivery will be guaranteed and CPU utilization will be optimum but this create a pipeline where the requests start queuing. Because of the Single-Threaded connection if the client push the button 5, he receive all of the messages waiting in the queue.
Client push 1 + Name to join the group, 2 + Message to send a message to the group, 3 + NewName to change their name, 4 to left the group, 5 to receive all the messages.
Note: The work was tested and checked in localhost.

## Installation

Download [server.py](https://github.com/benazoulaydev/Networking/blob/master/1%20-%20UDP/server.py) and [client.py](https://github.com/benazoulaydev/Networking/blob/master/1%20-%20UDP/client.py).



## Usage
Launch the server:
Choose a port for the server to listen (here 12345):
```bash
python3 server.py 12345
```


For each client:
specify ip of the server here 127.0.0.1 because we are in localhost and the port that the server listen to here 12345.
```bash
python3 client.py 127.0.0.1 12345 
```


## License
[MIT](https://choosealicense.com/licenses/mit/)
