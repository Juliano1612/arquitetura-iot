import sys, socket, json

ID = int(sys.argv[1])
HOST = 'localhost'
PORT = 8090 + ID
neighbors = []

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def recvRouteTable():
	connection, address = mySocket.accept()
	msgBuf = connection.recv(1024)
	if len(msgBuf) > 0:
		print(msgBuf)

def recvMessage():
	print 'recvMessage'

def sendMessage():
	print 'sendMessage'

def populateNeighborsList():
	for arg in  sys.argv[2:]:
		neighbors.append((int(arg),8090+int(arg)))
	print ID, ' -> ',neighbors


def init():
	#see neighbors
	populateNeighborsList()
	#init node listener
	mySocket.bind((HOST, PORT))
	mySocket.listen(5)
	#wait for route table
	# recvRouteTable()
	#wait messages
	while True:
		print('WAITING ', ID)
		connection, address = mySocket.accept()
		msgBuf = connection.recv(1024)
		print('MSG LEN', len(msgBuf), ' ID ', ID)
		if len(msgBuf) > 0:
			# recvMessage()
			print msgBuf


init()
