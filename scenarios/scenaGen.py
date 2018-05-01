import sys, random

f = open('scenario'+sys.argv[1], 'w')

for i in range(0,int(sys.argv[2])):
    r = random.sample(range(0, int(sys.argv[3])), 2)
    f.write(str(r[0])+ ' ' + str(r[1]) + ' oi'+str(i) +'\n' )

f.close()