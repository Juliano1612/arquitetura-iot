import sys, socket, json

ID = int(sys.argv[1])
HOST = 'localhost'
PORT = 8090 + ID
routeTable = None

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def recvMessage(msg):
	#message reached the destination
	if int(msg['R']) == ID:
		if msg['M'].startswith('RESP'):
			print 'ID: ', str(ID),' RESPONSE RECEIVED: ', msg['M']
		else:
			print 'ID: ', str(ID),' REQUEST RECEIVED: ', msg['M']
			msg['M'] = 'RESP' + msg['M']
			msg['S'], msg['R'], msg['GS'], msg['GR'] = msg['R'], msg['S'], msg['GR'], msg['GS']
			sendMessage(msg)
	else:
		#print 'ID: ', str(ID),' resending message'
		sendMessage(msg)

def sendMessage(msg):
	clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	by = routeTable[int(msg['R'])]
	try:
		if by == ID:
			clientsocket.connect(('localhost', 8090+int(msg['R'])))
		else:
			clientsocket.connect(('localhost', 8090+by))
	except:
		print 'ERROR: cannot stablish connection'	
	#print 'ID: ', str(ID),' resending message to ', str(routeTable[int(msg['R'])])
	clientsocket.send(str(msg))
	

def populateNeighborsList():
	global routeTable
	argument = ''
	for arg in  sys.argv[2:]:
		argument += arg
	routeTable = eval(argument)
	#print 'ID: ', str(ID), ' -> ' ,routeTable


def init():
	print 'NODE ', str(ID), ' INITIALIZED'
	#see neighbors
	populateNeighborsList()
	#init node listener
	try:
		mySocket.bind((HOST, PORT))
		mySocket.listen(20)
	except:
		print 'ERROR: port ', str(8090+ID), ' not available'
	#wait messages
	while True:
		connection, address = mySocket.accept()
		msgBuf = connection.recv(256)
		if len(msgBuf) > 0:
			#print 'ID: ', str(ID) , ' MSG: ', msgBuf
			recvMessage(eval(msgBuf))


init()