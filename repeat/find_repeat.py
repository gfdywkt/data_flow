import copy
import math
fin = open('./md5_files/md5_sorted','r')
fout = open('./same/15','w')

cnt = 0
last = ''
for k in fin:
	line = k.strip().split('\t')
	if line[1] == last:
		print >> fout,line[0]
	last = line[1]

fout.close()
fin.close()
