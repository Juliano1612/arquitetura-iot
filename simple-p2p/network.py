import sys, os, socket, threading, time
from multiprocessing import Pool
from subprocess import call
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

nodeList = []
lines = []
commandList = []
graph = nx.Graph()
pred = None
dist = None
mapper = {'id':[], 'group':[], 'color':[]}

def createJSON(line):
	line = line.split()
	msg = '{\'S\':\''+str(line[0])+'\',\'GS\':\''+ mapper['group'][mapper['id'].index(int(line[0]))] +'\',\'R\':\''+str(line[1])+'\',\'GR\':\''+ mapper['group'][mapper['id'].index(int(line[1]))]+'\',\'M\':\''+ str(line[2])+'\'}'
	#print msg
	return msg

def sendMessages():
	global mapper
	msgsFile = open('../scenarios/scenario'+sys.argv[2], 'r')
	for line in msgsFile:
		msg = eval(createJSON(line))
		try:
			clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			clientsocket.connect(('localhost', 8090+int(msg['S'])))
			clientsocket.send(str(msg))
			time.sleep(0.1)
		except:
			print "ERROR: cannot stablish connection"

def createNodes():
	Pool(len(graph)).map(os.system, commandList)


def createAndInitNetwork():
	#draw and show graph
	mapper['color']= np.array(map(ord, mapper['group']))
	nx.draw(graph, with_labels=True, node_color=mapper['color'], cmap=plt.cm.Blues)
	#plt.show()
	plt.savefig('../networks/network'+ sys.argv[1] +'.png')
	#calculate shortest path between all nodes
	pred, dist =  nx.floyd_warshall_predecessor_and_distance(graph)
	for p in pred:
		commandCreate = 'python node.py ' + str(p) + ' ' + mapper['group'][p] + ' ' + sys.argv[1] + ' ' + sys.argv[2] + ' ' + str(pred[p])
		commandList.append(commandCreate)
		
	#clear ports to create nodes
	clearPort = 'sudo fuser -k -n tcp '
	for g in nx.nodes(graph):
		clearPort = clearPort + str(8090+g) + ' '
	print clearPort
	os.system(clearPort)

	t = threading.Thread(target=(createNodes), args=())
	t.start()
	time.sleep(1)


def init():
	f = open('../results/simulation_network'+sys.argv[1]+'_scenario'+sys.argv[2], 'w')
	#f.write(sys.argv[2]+'\n')
	configFile = open('../networks/network'+sys.argv[1], 'r')
	for line in configFile:
		line = line.split()
		#pop first element to reference
		first = (line.pop(0)).split(':')
		graph.add_node(int(first[0]))
		nodeList = [(int(first[0]), int(first[0]))]
		mapper['id'].append(int(first[0]))
		mapper['group'].append(first[1])
		line = map(int, line)
		for n in line:
			nodeList.append((int(first[0]), n))
		# print nodeList
		graph.add_edges_from(nodeList)
init()
createAndInitNetwork()
sendMessages()