import sys, os, socket, threading, time
from multiprocessing import Pool
from subprocess import call
import networkx as nx
import matplotlib.pyplot as plt

nodeList = []
commandList = []
graph = nx.Graph()
pred = None
dist = None


def createNodes():
	Pool(len(graph)).map(os.system, commandList)

def createAndInitNetwork():
	#draw and show graph
	nx.draw(graph, with_labels=True)
	# plt.show()
	#calculate shortest path between all nodes
	pred, dist =  nx.floyd_warshall_predecessor_and_distance(graph)
	#create thread to start nodes
	t = threading.Thread(target=createNodes, args=())
	t.start()
	#send route table to all nodes
	time.sleep(1)
	for p in pred:
		clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# passed = False
		# while not passed:
		try:
			# print "TRY"
			clientsocket.connect(('localhost', int(8090+p)))
			clientsocket.send(pred[p])
			# passed = True
			print('Foi ', p)
		except:
			print('n Foi ', p)
			# pass
def init():
	configFile = open(sys.argv[1], 'r')
	for line in configFile:
		#create node execution command
		command = 'python node.py '+ line
		commandList.append(command)
		#map all string elements to an int list
		line = map(int, line.split())
		#pop first element to reference
		first = line.pop(0)
		graph.add_node(first)
		nodeList = [(first, first)]
		for n in line:
			nodeList.append((first, n))
		# print nodeList
		graph.add_edges_from(nodeList)

init()
createAndInitNetwork()
