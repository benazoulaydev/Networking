# SHARE FILES WITH TCP

This Work enable to send files between multiple clients
via TCP connection. This is a Single-Threaded connection, so only, so delivery will be guaranteed and CPU utilization will be optimum but this create a pipeline where the requests start queuing.
Client in Mode 2 (see below): can type a word to search the file he wants, it display all the files with the word he yped in it and afterward he can choose which file he want to download (he types the number). 
## Installation

Download [server.py](https://github.com/benazoulaydev/Networking/blob/master/2%20-%20TCP/server.py) and [client.py](https://github.com/benazoulaydev/Networking/blob/master/2%20-%20TCP/client.py).



## Usage
Launch the server:
Choose a port for the server to listen (here 12345):
```bash
python3 server.py 12345
```
For the clients: first we have to know  the IP address of the server (here for exemple: 192.168.56.1). To do so type in the terminal in the same PC where you launch the server :
```bash
ifconfig
```
Then there is two options : if the client send file and if he receive files:
1- If the client send files:
the first parameter : 0, the second (the server ip): 192.168.56.1, the third (the server port): 12345, the fourth (the port that the client listen we can choose port for exemple): 11111. Note: all the files that the client want to send and the file client.py have to be on the same directory.
```bash
python3 client.py 0 192.168.56.1 12345 1111
```

2- if the client receive files:
the first parameter : 1, the second (the server ip): 192.168.56.1, the third (the server port): 12345
```bash
python3 client.py 1 192.168.56.1 12345
```

We can create as many clients as we want at the same time, for sending files and receiving (receive and send in Single-Threaded so all task is added to queue and executed one by one).

## License
[MIT](https://choosealicense.com/licenses/mit/)
