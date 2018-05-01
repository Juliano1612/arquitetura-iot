import sys

info = []

def statsNode():
    print '################ STATISTIC BY NODE ##################'
    print 'Node \t Sended Messages\tReceived Messages'
    sinfo = sorted(info, key=lambda tup: tup[0])
    for i in sinfo:
        print str(i[0]) + '\t\t' + str(i[2]) + '\t\t\t' + str(i[3])

def statsGroups():
    print '################ STATISTIC BY GROUP ##################'
    print 'Group \t Sended Messages\tReceived Messages'
    groups = {}
    for i in info:
        if i[1] in groups:
            groups[i[1]][0] += int(i[2])
            groups[i[1]][1] += int(i[3])
        else:
            groups[i[1]] = list((int(i[2]), int(i[3])))
    for key, values in groups.iteritems():
        print key + '\t\t' + str(values[0]) + '\t\t\t' + str(values[1])

def statsGeneral():
    print '################ GENERAL STATISTICS ##################'
    print 'Nodes \t Sended Messages\tReceived Messages'
    totSend, totRecv = 0,0
    for i in info:
        totSend+=int(i[2])
        totRecv+=int(i[3])
    print str(len(i)) + '\t\t' + str(totSend) + '\t\t\t' + str(totRecv)

def init():
    f = open('simulation_network'+sys.argv[1]+'_scenario'+sys.argv[2], 'r')
    print 'STATS OF ', f.readline()
    for line in f:
        data = line.split()
        info.append((data[0], data[1], data[2], data[3]))

init()
statsNode()
statsGroups()
statsGeneral()
