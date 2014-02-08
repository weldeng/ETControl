#logread
f = open('ETlog', 'r')
for line in f:
        print line,
lastline = line
f.close()
