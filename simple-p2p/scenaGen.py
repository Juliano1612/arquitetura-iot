import sys, random

f = open('cenario1.txt', 'w')

for i in range(0,int(sys.argv[1])):
    r = range(0, int(sys.argv[2]))
    f.write(str(random.choice(r))+ ' ' + str(random.choice(r)) + ' oi'+str(i) +'\n' )

f.close()