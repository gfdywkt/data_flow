#-*- encoding: utf-8 -*-
import os, string
import MySQLdb
import sys
import re
import jieba
import math
import multiprocessing
import time
import traceback
import json
reload(sys)
sys.setdefaultencoding('utf8')
  

def myprocess(st):
	print st + ' start'
	try:	
		filename = st  
		#if os.path.exists('./idf_files/' + filename):
		#	print 'end'
		#	return
		fout = open('./idf_files/' + filename,'w')
	
		try:
			# 因为代码在外网，这里处理了一些敏感信息
			conn = MySQLdb.connect(host='myhost',user='myuser',passwd='mypwd',db='mydb',charset='utf8')
		except Exception, e:
			print e
			sys.exit()
 
		cursor = conn.cursor()

		sql = 'set character_set_client = utf8'
		cursor.execute(sql)
	
		sql = 'select content from crawl where us_id>'+ st +' limit 100000'
		cursor.execute(sql)
		alldata = cursor.fetchall()
		cnt = 0
		idf = {}
		for k in alldata:
			content = k[0]
			dr = re.compile(r'<[^>]+>',re.S)
			content = dr.sub('',content)
			seg_list = list(jieba.cut(content))
			rec = {}
			for item in seg_list:
				if item not in rec:
					rec[item] = 1
					if item in idf:
						idf[item] += 1
					else:
						idf[item] = 1
			cnt += 1
			if cnt % 1000 == 0:
				print st + ' ' + str(cnt)
				print len(idf)
	
		for key in idf:
			# idf[key] = math.log10(10000/float(idf[key]))
			print >> fout, '%s\t%s' % (key,idf[key])

		conn.close()	
		fout.close()
		print 'end'
	except:
		print traceback.print_exc()

def calc_idf():
	#开16个进程同时计算每个词出现的次数
	pool = multiprocessing.Pool(processes = 16)
	for num in range(0, 31200000, 100000):
		pool.apply_async(myprocess, (str(num),))
	pool.close()
	pool.join()	

if __name__ == "__main__":
	calc_idf()
