import sys, socket, signal, fcntl

ID = int(sys.argv[1])
GROUP = sys.argv[2]
NSEND, NRCVD = 0, 0
HOST = 'localhost'
PORT = 8090 + ID
routeTable = None
confiableList = []

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def recvMessage(msg):
	global NRCVD
	cache = False
	#if isnt generated message
	if int(msg['S']) == ID:
		NRCVD -= 1
	if msg['T'] == 'RQ':
		#if the communication is from out and i'm from recv group and not have cache
		if msg['GS'] != msg['GR'] and GROUP == msg['GR'] and msg['L'] ==  '':
			msg['L'] = str(ID)
			if msg['S'] in confiableList:
				cache = True
			#print 'Im the cache of this message'
	elif msg['L'] == str(ID):
		#print 'I\'m the cache ' + str(ID)
		confiableList.append(msg['R'])

	#message reached the destination
	if int(msg['R']) == ID or cache:
		if msg['M'].startswith('RESP'):
			print 'ID: ', str(ID),' RESPONSE RECEIVED: ', msg['M']
		else:
			print 'ID: ', str(ID),' REQUEST RECEIVED: ', msg['M']
			msg['M'] = 'RESP' + msg['M']
			msg['S'], msg['R'], msg['GS'], msg['GR'], msg['T'] = msg['R'], msg['S'], msg['GR'], msg['GS'], 'RS'
			sendMessage(msg)
	else:
		#print 'ID: ', str(ID),' resending message'
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
	for arg in  sys.argv[5:]:
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
		st = open('../results/cache-group/simulation_network'+sys.argv[3]+'_scenario'+sys.argv[4], 'a')
		fcntl.flock(st, fcntl.LOCK_EX)
		st.write(str(ID)+' '+ GROUP + ' ' + str(NSEND) + ' ' + str(NRCVD) + '\n')
		fcntl.flock(st, fcntl.LOCK_UN)

init()