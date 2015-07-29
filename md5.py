#-*- encoding: utf-8 -*-
import os, string
import MySQLdb
import sys
import re
import math
import multiprocessing
import time
import operator
import os.path
import traceback
import hashlib
reload(sys)
sys.setdefaultencoding('utf8')
  

def myprocess(st):
	print st + ' start'	
	rootdir = './tfidf_sorted/'
	outdir = './md5_files/'
	dic = {}
	fin = open(rootdir + st, 'r')
	fout = open(outdir + st, 'w')
	for k in fin:
		try:
			line = k.strip().split('\t')
			content = ''.join(line[1:])					
			md5 = hashlib.md5(content.encode('utf-8')).hexdigest()
			print >> fout,'%s\t%s' % (line[0],md5)
		except:
			continue
	fout.close()
	fin.close()
	print 'end'

def md5():
	# 把所有关键词及其对应的权值hash成一个md5串
	pool = multiprocessing.Pool(processes = 8)
	for num in range(0, 31200000, 10000):
		pool.apply_async(myprocess, (str(num),))
	pool.close()
	pool.join()	

if __name__ == "__main__":
	md5()
