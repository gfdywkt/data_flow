import os
import os.path
rootdir = './idf_files/'
fout = open('all_data','w')
dic = {}
for parent,dirnames,filenames in os.walk(rootdir):
	for filename in filenames:
		print 'doing ./idf_files/' + filename
		fin = open('./idf_files/' + filename, 'r')
		for k in fin:
			line = k.strip().split('\t')
			if len(line) == 2:	
				if line[0] not in dic:
					dic[line[0]] = int(line[1])
				else:
					dic[line[0]] += int(line[1])
		fin.close()

for key in dic:
	print >> fout, '%s\t%s' % (key,dic[key])

fout.close()
