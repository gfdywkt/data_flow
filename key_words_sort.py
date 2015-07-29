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
reload(sys)
sys.setdefaultencoding('utf8')
  

def myprocess(st):
	print st + ' start'	
	rootdir = './tf_files/'
	outdir = './tfidf_sorted/'
	dic = {}
	fin = open(rootdir + st, 'r')
	fout = open(outdir + st, 'w')
	for k in fin:
		try:
			line = k.strip().split('\t')
			rec = {}
			for i in range(1,31,2):
				rec[line[i]] = line[i+1]					
			rec_sorted = sorted(rec.iteritems(), key=operator.itemgetter(0), reverse=True)
			print >> fout, '%s' % (line[0]),
			for item in rec_sorted:
				print >> fout,'\t%s\t%s' % (item[0],item[1]),
			print >> fout,''
		except:
			continue
	fout.close()
	fin.close()
	print 'end'

def sort_key_words():
	# 把每篇文章的关键词按照字典序排序便于之后比较
	pool = multiprocessing.Pool(processes = 8)
	for num in range(0, 31200000, 10000):
		pool.apply_async(myprocess, (str(num),))
	pool.close()
	pool.join()	

if __name__ == "__main__":
	sort_key_words()
