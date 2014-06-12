#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database import Database

class Discovery():
	'''special method to produces seeds url and send it to sources'''
	def __init__(self, params):
		#connexion à la base du projet
		self.db = Database(params['project'])
	def config(self,params):
		#configuration
		self.query = "\""+params['query'][-1]+"\""
		self.path = params['file'][-1]
		self.key = params['key'][-1]
		self.seeds = []


		# tables particulières au crawl
		self.db.use_colls()
		# self.db.sources = self.db.use_coll('sources')
		# self.db.queue = self.db.use_coll('queue')
		# self.db.results = self.db.use_coll('results')
		# self.db.logs = self.db.use_coll('logs')
		

		#constitution de la base sources
		# print "Finding new seeds with query"
		# if self.key is None:
		# 	self.key = "J8zQNrEwAJ2u3VcMykpouyPf4nvA6Wre1019v/dIT0o"
		
		# if self.query is not None:
		# 	if self.path is not None:
		# 		print self.get_local()
		# 	if self.key is not None:
		# 		self.get_bing()
		# 	self.send_to_sources()
		# else:
		# 	"No query found in your projet %s" %params['project']
		
		self.send_to_queue()


	def send_to_sources(self):	
		for n in self.seeds:
			#first send to sources
			#db.sources.insert({"url":n, "date": datetime.datetime.today(), "mode":"discovery"} for n in self.seeds if n is not None)
			self.db.sources.update({"url":n, "mode":"discovery"}, {"$push": {"date":datetime.datetime.today()}}, upsert=True)
		return self

	def send_to_queue(self):
		sources_queue = [{"url":url} for url in self.db.sources.distinct("url")]
		if len(sources_queue) != 0:
			#db.sources.update([{"url":n}, {'$push': {"date": datetime.datetime.today()}}, upsert=True)
			self.db.queue.insert(sources_queue)
		return self

	def get_bing(self):
		''' Method to extract results from BING API (Limited to 5000 req/month). ''' 
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
			
			for e in r.json()['d']['results']:
				#print e['Url'] 
				self.seeds.append(e['Url']) 
			self.seeds = list(set(self.seeds))
			print len(self.seeds),"results from Bing API"
			return True
		
		except Exception as e:
			print "Error", e, e.args
			self.status_code = -1
			self.error_type = "Error fetching results from BING API, check your credentials. May not exceed the 5000req/month limit (%s)" %e.args
			return False

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
	def __init__(self,params):
		'''simple producer : insert from sources database to processing queue'''
		print "Running a crawl on existing database"
		self.db = Database(params['project'])
		self.db.create_colls()
		sources_queue = [{"url":url, "date": datetime.datetime.today()} for url in self.db.sources.distinct("url") if url not in self.db.queue.distinct("url")]
		if len(sources_queue) != 0:
			self.db.queue.insert(sources_queue)
		