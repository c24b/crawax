#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Crawtext.

Usage:
	crawtext_4.py <project> crawl <query> [--repeat]
	crawtext_4.py <project> discover <query> [--file=<filename> | --key=<bing_api_key> | --file=<filename> --key=<bing_api_key>] [--repeat]
	crawtext_4.py <project> start <query>
	crawtext_4.py <project> stop
	crawtext_4.py (-h | --help)
  	crawtext_4.py --version

Options:
	--file Complete path of the sourcefile.
	--key  Bing API Key for Search.
	--repeat Scheduled task for every monday @ 5:30.
	-h --help Show usage and Options.
	--version Show versions.  
'''
#__all__ = ['crawtext']

#from __future__ import print_function
from os.path import exists
import sys
import requests
import json
import re
#import threading
#import Queue
import pymongo
from pymongo import MongoClient
from pymongo import errors
from bs4 import BeautifulSoup as bs
from urlparse import urlparse
from random import choice
#from pygoose import *
from tld import get_tld
import datetime
import __future__
from docopt import docopt
from abpy import Filter
#from scheduler import *
from database import Database

unwanted_extensions = ['css','js','gif','asp', 'GIF','jpeg','JPEG','jpg','JPG','pdf','PDF','ico','ICO','png','PNG','dtd','DTD', 'mp4', 'mp3', 'mov', 'zip','bz2', 'gz', ]	
adblock = Filter(file('easylist.txt'))
			
class Page(object):
	'''Page factory'''
	def __init__(self, url, query):
		self.url = url
		self.query = query
		self.status = None
		self.error_type = None
		self.info = {}
		self.outlinks = None

	def check(self):
		'''Bool: check the format of the next url compared to curr url'''
		if self.url is  None or len(self.url) <= 1 or self.url == "\n":
			self.error_type = "Url is empty"
			return False
		elif (( self.url.split('.')[-1] in unwanted_extensions ) and ( len( adblock.match(self.url) ) > 0 ) ):
			self.error_type="Url has not a proprer extension or page is an advertissement"
			return False
		else:
			return True
		
	def request(self):
		'''Bool request a webpage: return boolean and update src'''
		try:
			requests.adapters.DEFAULT_RETRIES = 2
			user_agents = [u'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1', u'Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2', u'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0', u'Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00']
			headers = {'User-Agent': choice(user_agents),}
			proxies = {"https":"77.120.126.35:3128", "https":'88.165.134.24:3128', }
			self.req = requests.get((self.url), headers = headers,allow_redirects=True, proxies=proxies, timeout=5)
			try:
				self.src = self.req.text
				return True	
			except Exception, e:
				self.error_type = "Request answer was not understood %s" %e
				return False
			else:
				self.error_type = "Not relevant"
				return False
		
		except requests.exceptions.MissingSchema:
			self.error_type = "Incorrect url %s" %self.url
			return False
		except Exception as e:
			self.error_type = str(e)
			return False
		
	def control(self):
		'''Bool control the result of request return a boolean'''
		#Content-type is not html 
		
		if 'text/html' not in self.req.headers['content-type']:
			self.error_type="Content type is not TEXT/HTML"
			return False
		#Error on ressource or on server
		elif self.req.status_code in range(400,520):
			self.error_type="Connexion error"
			return False
		#Redirect
		#~ elif len(self.req.history) > 0 | self.req.status_code in range(300,320): 
			#~ self.error_type="Redirection"
			#~ self.bad_status()
			#~ return False
		else:
			return True	
	
	def extract(self):
		'''Dict extract content and info of webpage return boolean and self.info'''
		try:
			#using Goose extractor
			g = Goose()
			article = g.extract(raw_html=self.src)
			#filtering relevant webpages
			if self.filter() is True:
				self.outlinks = set([self.clean_url(url=e.attrs['href']) for e in bs(self.src).find_all('a', {'href': True})])
			self.info = {	
						"url":self.url,
						"domain": get_tld(self.url),
						"outlinks": list(self.outlinks),
						"backlinks":[n for n in self.outlinks if n == self.url],
						"texte": article.cleaned_text,
						"title": article.title,
						"meta_description":bs(article.meta_description).text
						}
			return self.info
		except Exception, e:
			self.error_type = str(e)
			return False	
					
	def filter(self):
		'''Bool Decide if page is relevant and match the correct query. Reformat the query properly: supports AND, OR and space'''
		if 'OR' in self.query:
			for each in self.query.split('OR'):
				query4re = each.lower().replace(' ', '.*')
				if re.search(query4re, self.src, re.IGNORECASE) or re.search(query4re, self.url, re.IGNORECASE):
					return True

		elif 'AND' in self.query:
			query4re = self.query.lower().replace(' AND ', '.*').replace(' ', '.*')
			return bool(re.search(query4re, self.src, re.IGNORECASE) or re.search(query4re, self.url, re.IGNORECASE))

		else:
			query4re = self.query.lower().replace(' ', '.*')
			return bool(re.search(query4re, self.src, re.IGNORECASE) or re.search(query4re, self.url, re.IGNORECASE))
			 	
		
	def bad_status(self):
		'''create a msg_log {"url":self.url, "error_code": self.req.status_code, "error_type": self.error_type, "status": False}'''
		try:
			assert(self.req) 
			if self.req.status_code is not None and self.error_type is not None:
				return {"url":self.url, "error_code": self.req.status_code, "type": self.error_type, "status": False}
			elif self.req is None and self.error_type is not None:
				return {"url":self.url, "error_code": None, "type": self.error_type, "status": False}
			elif self.req is not None and self.error_type is None:	
				return {"url":self.url, "error_code": None, "type": self.req.status_code, "status": False}
			else:
				return {"url":self.url,"status": False}
		except Exception:
			return {"url":self.url, "error_code": "Request Error", "type": self.error_type, "status": False}
	def clean_url(self, url):
		''' utility to normalize url and discard unwanted extension : return a url or None'''
		#ref tld: http://mxr.mozilla.org/mozilla-central/source/netwerk/dns/effective_tld_names.dat?raw=1
		if url not in [ "#","/", None, "\n", "",] or url not in 'javascript':
			self.netloc = urlparse(self.url).netloc
			uid = urlparse(url)
			#if next_url is relative take previous url netloc
			if uid.netloc == "":
				if len(uid.path) <=1:
					return None			
				elif (uid.path[0] != "/" and self.netloc[-1] != "/"):
					clean_url = "http://"+self.netloc+"/"+uid.path
				else:
					clean_url = "http://"+self.netloc+uid.path
			else:
				clean_url = url
			return clean_url
		else:
			return None			

class Discovery():
	'''special method to produces seeds url and send it to sources'''
	def __init__(self, db_name, query, path=None, api_key=None):
		#constitution de la base
		db = Database(db_name)
		db.create_tables()
		self.seeds = []
		self.path = path
		self.key = api_key
		if query is not None:
			if self.path is not None:
				self.get_local()
			if query is not None:
				self.get_bing()
		self.send_to_sources(db, query)
		self.send_to_queue(db)

	def send_to_sources(self, db, query):	
		for n in self.seeds:
			#first send to queue
			db.sources.insert({"url":n, "crawl_date": datetime.datetime.today(), "mode":"discovery"} for n in self.seeds if n is not None)

			# p = Page(n, query)
			# if p.check() and p.request() and p.control() and p.extract() and p.filter():
			# 	#send it to results
			# 	if url not in db.results
			# 	db.results.insert(p.info)
			# 	#send next urls to queue
			# 	for url in p.outlinks:
			# 		if url is not None or url not in db.queue.distinct("url"):
			# 			db.queue.insert({"url":url})
			# else:
			# 	#problematic sources are automatically sent to log
			# 	db.log.insert(p.bad_status())  
		#Todo: integrate it into mail report				
		# print "Nb de sources", db.sources.count()
		# print "Nb urls en traitement", db.queue.count()
		# print "nb erreur", db.log.count()
		return db

	def send_to_queue(self, db):
		sources_queue = [{"url":url, "date": datetime.datetime.today()} for url in db.sources.distinct("url") if url not in db.queue.distinct("url")]
		if len(sources_queue) != 0:
			db.queue.insert(sources_queue)
		return db
	def get_bing(self):
		''' Method to extract results from BING API (Limited to 5000 req/month). ''' 
		print "Searching on Bing"
		try:
			r = requests.get(
				'https://api.datamarket.azure.com/Bing/Search/v1/Web', 
				params={
					'$format' : 'json',
					'$top' : 50,
					'Query' : '\'%s\'' % self.query,
				},
				auth=(self.key, self.key)
				)
			for e in r.json()['d']['results']:
				self.seeds.append(e['Url']) 
			self.seeds = list(set(self.seeds))
			print len(self.seeds), results
			return True
		except:

			self.error_type = "Error fetching results from BING API, check your credentials. May exceed the 5000req/month limit "
			print self.error_type
			return False

	def get_local(self):
		''' Method to extract url list from text file'''
		print "Harvesting the sources you gave him"
		try:
			for url in open(self.path).readlines():
				self.seeds.append(url) 
			self.seeds = list(set(self.seeds))
			return True
		except:
			self.error_type = "Error fetching results from file %s. Check if file exists" %self.path
			return False			

class Sourcing():
	'''From an initial db sources send url to queue'''
	def __init__(self,db_name):
		'''simple producer : insert from sources database to processing queue'''
		db = Database(db_name)
		db.create_tables()
		sources_queue = [{"url":url, "date": datetime.datetime.today()} for url in db.sources.distinct("url") if url not in db.queue.distinct("url")]
		if len(sources_queue) != 0:
			db.queue.insert(sources_queue)

def crawler(docopt_args):
	start = datetime.datetime.now()
	db_name=docopt_args['<project>']
	query=docopt_args['<query>']
	'''the main consumer from queue insert into results or log'''
	db = Database(db_name)
	db.create_tables()
	print db.queue.count()
	while db.queue.count > 0:
		print "beginning crawl"
		print db.sources.count()
		print db.queue.count()
		for url in db.queue.distinct("url"):	
			if url not in db.results.find({"url":url}) or url not in db.log.find({"url":url}):
				p = Page(url, query)
				if p.check() and p.request() and p.control() and p.extract():
					db.results.insert(p.info)
					if p.outlinks is not None:
						try:
							for n_url in p.outlinks:
								if n_url not in db.queue.find({"url":n_url}): 
									if n_url not in db.results.find({"url":n_url}) or n_url not in db.log.find({"url":n_url}):
										db.queue.insert({"url":n_url})
						except pymongo.errors:
							db.log.insert(({"url":url, "error_type": "pymongo error inserting outlinks", "status":False}))
				else:
					db.log.insert(p.bad_status())
			db.queue.remove({"url": url})
			# print "En traitement", self.db.queue.count()
			# print "Resultats", self.db.results.count()
			# print "Erreur", self.db.log.count()
			if db.queue.count() == 0:
				break
		if db.queue.count() == 0:
				break
	end = datetime.datetime.now()
	elapsed = end - start
	print "crawl finished, %i results and %i sources are stored in Mongo Database: %s in %s" %(db.results.count(),db.sources.count(),db_name, elapsed)

def crawtext(docopt_args):
	''' main crawtext run by command line option '''
	if docopt_args['discover'] is True:
		print "discovery"
		Discovery(db_name=docopt_args['<project>'],query=docopt_args['<query>'], path=docopt_args['--file'], api_key=docopt_args['--key'])
		Sourcing(db_name=docopt_args['<project>'])
		crawler(docopt_args)
		# if docopt_args['--repeat']:
		# 	schedule(crawler, docopt_args)
		# 	return sys.exit()
	elif docopt_args['crawl'] is True:
		Sourcing(db_name=docopt_args['<project>'])
		crawler(docopt_args)
		# if docopt_args['--repeat']:
			# schedule(crawler, docopt_args)
			# return sys.exit()
	elif docopt_args['stop']:
		# unschedule(docopt_args)
		print "Process is stopped"
		return
	elif docopt_args['start']:
		'''Option Start here (and for the moment) is just a defaut activate of the crawl using defaut api key and basic query'''
		Discovery(db_name=docopt_args['<project>'], query=docopt_args['<query>'], api_key="J8zQNrEwAJ2u3VcMykpouyPf4nvA6Wre1019v/dIT0o")
		Sourcing(db_name=docopt_args['<project>'])
		print "DB Sources is created with a first search on BING based on your project name"
		#schedule(crawler, docopt_args)
		return
	else:
		print "No command supplied, please check command line usage and options."
		return sys.exit() 

if __name__ == "__main__":
	args = docopt(__doc__)
	crawtext(args)
	sys.exit()

