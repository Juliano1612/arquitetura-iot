import sys, socket, signal, fcntl

ID = int(sys.argv[1])
GROUP = sys.argv[2]
NSEND, NRCVD = 0, 0
HOST = 'localhost'
PORT = 8090 + ID
routeTable = None

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def recvMessage(msg):
	global NSEND
	#message reached the destination
	if int(msg['R']) == ID:
		if msg['M'].startswith('RESP'):
			print 'ID: ', str(ID),' RESPONSE RECEIVED: ', msg['M']
		else:
			print 'ID: ', str(ID),' REQUEST RECEIVED: ', msg['M']
			msg['M'] = 'RESP' + msg['M']
			msg['S'], msg['R'], msg['GS'], msg['GR'] = msg['R'], msg['S'], msg['GR'], msg['GS']
			NSEND += 1
			sendMessage(msg)
	else:
		#print 'ID: ', str(ID),' resending message'
		NSEND += 1
		sendMessage(msg)

def sendMessage(msg):
	global NSEND
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
	NSEND += 1
	clientsocket.send(str(msg))
	

def populateNeighborsList():
	global routeTable
	argument = ''
	for arg in  sys.argv[3:]:
		argument += arg
	routeTable = eval(argument)
	#print 'ID: ', str(ID), ' -> ' ,routeTable


def init():
	global NSEND, NRCVD
	print 'NODE ', str(ID), ' GROUP ', GROUP ,' INITIALIZED'
	#see neighbors
	populateNeighborsList()
	#init node listener
	try:
		mySocket.bind((HOST, PORT))
		mySocket.listen(20)
	except:
		print 'ERROR: port ', str(8090+ID), ' not available'
	#wait messages
	try:
		while True:
			connection, address = mySocket.accept()
			msgBuf = connection.recv(256)
			if len(msgBuf) > 0:
				#print 'ID: ', str(ID) , ' MSG: ', msgBuf
				NRCVD += 1
				recvMessage(eval(msgBuf))
	finally:
		st = open('simulation_data.txt', 'a')
		fcntl.flock(st, fcntl.LOCK_EX)
		st.write(str(ID)+' '+ GROUP + ' ' + str(NSEND) + ' ' + str(NRCVD) + '\n')
		fcntl.flock(st, fcntl.LOCK_UN)

init()