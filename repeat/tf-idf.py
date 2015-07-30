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
import operator
reload(sys)
sys.setdefaultencoding('utf8')
  

def myprocess(st):
	print st + ' start'	
	fout = open('./tf_files/' + st,'w')
	try:
		conn = MySQLdb.connect(host='10.146.19.233',user='crawler',passwd='xxxxxx',db='crawler_all',charset='utf8')
	except Exception, e:
		print e
		conn.close()
		sys.exit()
 
	cursor = conn.cursor()

	sql = 'set character_set_client = utf8'
	cursor.execute(sql)
	
	sql = 'select us_id,content from crawl where us_id >'+ st +' limit 10000'
	cursor.execute(sql)
	alldata = cursor.fetchall()
	cnt = 0
	# 对于每篇招中标信息计算tf-idf
	for k in alldata:
		try:
			id = k[0]
			content = k[1]
			dr = re.compile(r'<[^>]+>',re.S)
			content = dr.sub('',content)
			seg_list = list(jieba.cut(content))
			tf = {}
			tf_idf = {}
			# 统计tf值
			for item in seg_list:
				if item not in tf:
					tf[item] = 1
				else:
					tf[item] += 1
			# 对应idf表计算出tf-idf值
			for key in tf:
				key = key.strip('\t').strip('\n').strip()
				if key == '':
					continue
				if key.encode('utf8') in idf:
					tf_idf[key] = tf[key] * idf[key.encode('utf8')]
				else:
					tf_idf[key] = tf[key] * 7.157039

			# 把单词按tf-idf排序，取前15个词作为关键词
			tfidf_sorted = sorted(tf_idf.iteritems(), key=operator.itemgetter(1), reverse=True)
			print >> fout, id,
			list_len = len(tfidf_sorted)
			if list_len >= 15:
				list_len = 15
			for i in range(list_len):
				print >> fout, '\t%s\t%s' % (tfidf_sorted[i][0],tfidf_sorted[i][1]),
			print >> fout, ''
			cnt += 1
			if cnt % 500 == 0:
				print st + ' ' + str(cnt)
		except:
			continue
	cursor.close()
	conn.close()
	fout.close()
	print 'end'

def calc_tfidf(idf):
	#分16个进程计算tf-idf值
	pool = multiprocessing.Pool(processes = 16)
	for num in range(0, 31200000, 10000):
		pool.apply_async(myprocess, (str(num),))
	pool.close()
	pool.join()	

if __name__ == "__main__":
	# 读入每个词的出现总次数，存入idf字典
	all_words_sum = open('all_data','r')
	global idf
	idf = {}
	cnt = 0
	for k in all_words_sum:
		line = k.strip().split('\t')
		idf[line[0]] = line[1]
		cnt += 1
		if cnt % 10000 == 0:
			print cnt
	all_words_sum.close()
	
	# 计算每个单词的idf值
	cnt = 0
	for key in idf:
		idf[key] = math.log10(14356184/(float(idf[key]) + 1.0))
		cnt += 1
		if cnt % 10000 == 0:
			print cnt

	calc_tfidf(idf)
