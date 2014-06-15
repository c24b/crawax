#!/usr/bin/env python
# -*- coding: utf-8 -*
# file /crawler/crawler.py

from datetime import datetime
from database import Database
from page import PageFactory

import pymongo
def crawler(name, query):
	'''Main Crawler for Job'''
	start = datetime.now()
	print name
	db = Database(name)
	db.create_colls()
	#get from source
	for n in db.sources.find():
		if n["url"] not in db.queue.distinct("url"):
			db.queue.insert(n)
		
	while db.queue.count > 0:

		print "Beginning crawl"
		# print "Number of seeds urls in sources databases:", db.sources.count()
		# print "Number of pending url to inspect:", len(db.queue.distinct("url"))
		for url in db.queue.distinct("url"):
			
			if url not in db.results.find({"url":url}):
				print url
				p = PageFactory(url, query)
				page = p.create()
				print page.type
			
				
				#print "Links", p.outlinks
				#db.results.update(p.info, {'$push': {"date": datetime.today()}}, upsert=True)
				#db.results.insert(p.info)
				# if p.outlinks is not None:
				# 	try:
				# 		for n_url in p.outlinks:
				# 			if n_url is not None or  n_url not in db.queue.find({"url":n_url}) or n_url not in db.results.find({"url":n_url}) or n_url not in db.log.find({"url":n_url}):
				# 				# Checking correct url before is problematic
				# 				# next_p = Page(n_url, query)
				# 				# if next_p.clean_url(p.url) is not None:
				# 				print n_url
				# 				db.queue.insert({"url":n_url})
				# 	except mongo_err:
				# 		db.log.udpate({"url":url, "error_type": "pymongo error inserting outlinks", "query": self.query, "status":False},{'$push': {"date": datetime.today()}}, upsert=True)
				# elif p.error_type != 0:
				# 	''' if the page is not relevant do not store in db'''
				# 	db.log.update(p.bad_status(),{'$push':{"date": datetime.today()}}, upsert=True)
				# else:
				# 	continue

			db.queue.remove({"url": url})
			if db.queue.count() == 0:
				print db.stats()
				break
			
		if db.queue.count() == 0:
			print db.stats()		
			break
		

	end = datetime.now()
	elapsed = end - start
	print "crawl finished, %i results and %i sources are stored in Mongo Database: %s in %s" %(db.results.count(),db.sources.count(),name, elapsed)
	return True

