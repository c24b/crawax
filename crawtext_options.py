#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database import Database
import datetime
import requests

class Discovery():
	'''special method to produces seeds url and send it to sources'''
	def __init__(self, db_name, query, path=None, api_key=None):
		#constitution de la base
		self.db = Database(db_name)
		self.db.create_tables()
		self.seeds = []
		self.path = path
		self.key = api_key
		self.query = query
		if self.query is not None:
			if self.path is not None:
				self.get_local()
			if query is not None and api_key is not None:
				self.get_bing()
		self.send_to_sources(self.db, query)
		self.send_to_queue(self.db)

	def send_to_sources(self, db, query):	
		for n in self.seeds:
			#first send to sources
			#db.sources.insert({"url":n, "date": datetime.datetime.today(), "mode":"discovery"} for n in self.seeds if n is not None)
			db.sources.update({"url":n, "mode":"discovery"}, {'$push': {"date": datetime.datetime.today()}}, upsert=True)
		return db

	def send_to_queue(self, db):
		sources_queue = [{"url":url} for url in db.sources.distinct("url")]
		if len(sources_queue) != 0:
			#db.sources.update([{"url":n}, {'$push': {"date": datetime.datetime.today()}}, upsert=True)
			db.queue.insert(sources_queue)
		return db
	def get_bing(self):
		''' Method to extract results from BING API (Limited to 5000 req/month). ''' 
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
		# except:

		# 	self.error_type = "Error fetching results from BING API, check your credentials. May not exceed the 5000req/month limit "
		# 	print self.error_type
		# 	return False

	def get_local(self):
		''' Method to extract url list from text file'''
		print "Collecting url from sourcefile"
		try:
			for url in open(self.path).readlines():
				self.seeds.append(re.sub("\n", "", url)) 
			self.seeds = list(set(self.seeds))
			return True
		except Exception:
			self.status_code = -1
			self.error_type = "Error fetching results from file %s. Check if file exists" %self.path
			print self.error_type
			return False			

class Sourcing():
	'''From an initial db sources send url to queue'''
	def __init__(self,db_name):
		'''simple producer : insert from sources database to processing queue'''
		self.db = Database(db_name)
		self.db.create_tables()
		sources_queue = [{"url":url, "date": datetime.datetime.today()} for url in self.db.sources.distinct("url") if url not in self.db.queue.distinct("url")]
		if len(sources_queue) != 0:
			self.db.queue.insert(sources_queue)