#!/usr/bin/env python
# -*- coding: utf-8 -*
# file /crawler/crawler.py

from datetime import datetime
from database import Database
import pymongo
import requests

class Crawler(object):
	def __init__(self, params):
		self.project = params["project"]
		self.query = params["query"][-1]
		self.file = params["file"][-1]
		self.key = params["key"][-1]
		self.db = Database(params["project"])
		self.db.create_colls()
		self.sourcing = params["sourcing"]
		self.seeds = []

	def send_to_sources(self):	
		for n in self.seeds:
			self.db.sources.update({"url":n, "discovery": True}, {"$push": {"date":datetime.today()}}, upsert=False)
		return self.db

	def send_to_queue(self):
		#here we could filter out problematic urls
		sources_queue = [{"url":url} for url in self.db.sources.distinct("url")]
		if len(sources_queue) != 0:
			#db.sources.update([{"url":n}, {'$push': {"date": datetime.datetime.today()}}, upsert=True)
			self.db.queue.insert(sources_queue)
		return self
	def get_bing(self):
		''' Method to extract results from BING API (Limited to 5000 req/month). ''' 
		print "Bing!", self.query
		try:
			r = requests.get(
					'https://api.datamarket.azure.com/Bing/Search/v1/Web', 
					params={
						'$format' : 'json',
						'$top' : 100,
						'Query' : '\'%s\'' % self.query,
					},
					auth=(self.key, self.key)
					)

			print "Searching on Bing"
			for e in r.json()['d']['results']:
				#print e['Url'] 
				self.seeds.append(e['Url']) 
			self.seeds = list(set(self.seeds))
			print len(self.seeds),"results from Bing API"
			return True
		except Exception as e:
			print e
			self.status_code = -1
			self.error_type = "Error fetching results from BING API, check your credentials. May not exceed the 5000req/month limit (%s)" %e.args
			return False

	def get_local(self):
		''' Method to extract url list from text file'''
		print "Collecting url from sourcefile"
		try:
			for url in open(self.file).readlines():
				self.seeds.append(re.sub("\n", "", url)) 
			self.seeds = list(set(self.seeds))
			return True
		except Exception:
			self.status_code = -1
			self.error_type = "Error fetching results from file %s. Check if file exists" %self.file
			print self.error_type
			return False
	
	def discovery(self):	
		if self.sourcing is False:
			if self.file is not None:
				self.get_local()
			if self.query is not None and self.key is not None:
				self.get_bing()	
			else:
				print "No initial sources to load"
			self.send_to_sources()
		return self.send_to_queue()
		
	def crawl(self):
		self.discovery()
		print len([n for n in self.db.queue.find()])
		return 

		# while self.db.queue.count > 0:
		# 	for url in self.db.queue.distinct("url"):
		# 		print url

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

# if __name__ == "__main__":
