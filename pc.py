#coding=utf8
"""
# Author: jackson
# Created Time : Tue 23 Jun 2015 03:51:50 PM CST

# File Name: pc.py
# Description:

"""
dic = {}
fin = open('company_ganji1','r')
for k in fin:
	line = k.strip().split('\t')
	if (len(line[0]) > 12):
		dic[line[0]] = 1
fin.close()

fout = open('company_ganji1_pc','w')
for k in dic:
	print >> fout , k

fout.close()
