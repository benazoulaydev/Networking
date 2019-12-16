import socket, sys

def firstCase(addressT, message, userfilesdic):
	userfilesdic[addressT] = message[1:]

def seCase(userfilesdic, filename):
	#dictionary of key number, value of the client info (that send the file) not sorted
	dictnumber={}
	#indexes as key for dictionaries keydic
	i=1
	j=1
	#dictionary with key numbers and value the name of the file
	keyDic = {}
	#dictionary with key 1,2,3,4,5,6... , value: client info (that send the file)
	# sorted in lexicographic order with the name of the files
	sortedDicNumber={}
	#create the first 2 dictionaries, one with the index and file
	# the second with the index and client info(sender)
	for key in userfilesdic:
		arrFilesName = userfilesdic[key]
		portClient = arrFilesName[0]
		ipTupleClient = key
		arrFilesName = arrFilesName[1:]
		for file in arrFilesName:
			if filename in file:
				keyDic[i] = file
				#use of dictionary into another dictionary
				# to ease the access of ip, port, filename info
				dictnumber[i] ={"ip": ipTupleClient,"port": portClient,"file": file}
				i += 1
	#create a sorted dictionary keyDic by value (here sorted by the name of the files)
	s = [(k, keyDic[k]) for k in sorted(keyDic, key=keyDic.get)]
	#sort the dictnumber with the name of the files in lexicographic order
	for key, value in s:
		sortedDicNumber[j] = dictnumber[key]
		j+=1
	return sortedDicNumber

def main():
	userfilesdic = {}
	TCP_IP = '0.0.0.0'
	TCP_PORT = int(sys.argv[1])
	BUFFER_SIZE = 2048
	#create the server socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)
	while True:
		try:
			conn, addr = s.accept()
			# print("connection accepted")
			# print('New connection from:', addr)
			data = conn.recv(BUFFER_SIZE)
			if not data: continue
			decodeMsg = data.decode()
			decodeMsg = decodeMsg.split(",")
			#print("received:", decodeMsg)
			#first client case scenario, keep all the files of the client
			if decodeMsg[0] == "1":
				firstCase(addr, decodeMsg, userfilesdic)
			#second client case scenario to download  files of other clients
			elif decodeMsg[0] == "2":
				#get the dictionary dictnumber sorted by file name
				dictnumber = seCase(userfilesdic, decodeMsg[1])
				#print(dictnumber)
				#create variable to keep the name of the files
				NAME_FILES = ""
				#add them in lexicographic order since dictnumber is sorted lexicographically
				#for each key add the file name to the string
				for key in dictnumber:
					NAME_FILES += dictnumber[key]["file"]
					NAME_FILES += ","
				#remove the last separator of NAME_FILES ","
				NAME_FILES = NAME_FILES[:-1]
				#send the files name to the client
				if not conn:
					continue

				conn.send(NAME_FILES.encode())
				#receive which file he chooses
				numberFile = conn.recv(BUFFER_SIZE).decode()
				#access to the dictionary into the dictionary that
				# have key : ip, port, file
				clientdict = dictnumber[int(numberFile)]
				#get the tuple ip port (the port here was decided by the OS this is not the
				# port that the client listen to) of the client
				l = clientdict["ip"]
				#get the ip inisde the tuple
				ipClient = l[0]
				#get the port inside the tuple
				portClient = l[1]

				strHlp = ipClient + "," + str(portClient) + "," + clientdict["port"] + "," + clientdict["file"]
				conn.send(strHlp.encode())
				conn.close()
		except:
			continue



main()
