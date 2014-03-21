#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import exists
import sys
import requests
import json
import re
import threading
import Queue
import pymongo


from pymongo import MongoClient
from pymongo import errors
from bs4 import BeautifulSoup as bs
from urlparse import urlparse
from random import choice
from goose import Goose
from tld import get_tld
from datetime import datetime
import __future__


unwanted_extensions = ['css','js','gif','asp', 'GIF','jpeg','JPEG','jpg','JPG','pdf','PDF','ico','ICO','png','PNG','dtd','DTD', 'mp4', 'mp3', 'mov', 'zip','bz2', 'gz', ]	
from abpy import Filter
adblock = Filter(file('easylist.txt'))


class Database():
	def __init__(self, database_name):
		self.name = database_name
		client = MongoClient('mongodb://localhost,localhost:27017')
		self.db = client[self.name]
		#self.db.x = self.db[x]
		
	def __repr__(self, database_name):	
		return self.name
		
	def create_tables(self):
		self.results = self.db['results']
		self.queue = self.db['queue'] 
		self.log = self.db['log']
		self.sources = self.db['sources']
		return self
			
class Page(object):
	def __init__(self, url, query):
		self.url = url
		self.query = query
		self.status = None
		self.error_type = None
		self.info = {}
		self.outlinks = None

	def check(self, url=None):
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
		'''request a webpage: return boolean and update src'''
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
		'''control the result of request return a boolean'''
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
		'''extract content and info of webpage return boolean and self.info'''
		try:
			g = Goose()
			article = g.extract(raw_html=self.src)
			if self.filter() is True:
				self.outlinks = list(set([self.clean_url(url=e.attrs['href']) for e in bs(self.src).find_all('a', {'href': True})]))
			self.info = {	
						"url":self.url,
						"domain": get_tld(self.url),
						"outlinks": self.outlinks,
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
		'''Decide if page is relevant and match the correct query. Reformat the query properly: supports AND, OR and space'''
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
		'''create a msg_log {"url":self.url, "error_code": self.req.status_code, "type": self.error_type, "status": False}'''
		try:
			self.code = self.req.status_code
		except AttributeError:
			self.code = None
		return {"url":self.url, "error_code": self.code, "type": self.error_type, "status": False}
	
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

def InitSeeds(sources_list, db_name):
	#constitution de la base
	db = Database(db_name)
	db.create_tables()
	
	for n in liste:
		p = Page(n, query)
		if p.check() and p.request() and p.control() and p.extract() and p.filter():
			db.results.insert(p.info)
			db.sources.insert({"url":p.info["url"], "crawl_date": datetime.today()})
			for url in p.outlinks:
				if url is not None or url not in db.queue.distinct("url") or url not in db.results.distinct("url") or url not in db.log.distinct("url"):
					db.queue.insert({"url":url})
		else:
			db.log.insert(p.bad_status())  
					
	print "Nb de sources", db.sources.count()
	print "Nb urls en traitement", db.queue.count()
	print "nb erreur", db.log.count()
	return db

def Sourcing(db_name):
	db = Database(db_name)
	db.create_tables()
	sources_queue = [{"url":url} for url in db.sources.distinct("url") if url not in db.queue.distinct("url")]
	if len(sources_queue) != 0:
		yield db.queue.insert(sources_queue)
		 

def Crawler(db_name, query):
	db = Database(db_name)
	db.create_tables()
	print db.queue.count()
	while db.queue.count > 0:
		print "beginning crawl"
		for n in db.queue.distinct("url"):	
			if n not in db.results.distinct("url") or n not in db.log.distinct("url"):
				p = Page(n, query)
				if p.check() and p.request() and p.control() and p.extract():
					db.results.insert(p.info)
					if p.outlinks is not None:
						db.queue.insert([{"url":url} for url in p.outlinks 
											if url not in db.queue.distinct("url") 
											or url not in db.results.distinct("url") 
											or url not in db.log.distinct("url")
										])
				else:
					db.log.insert(p.bad_status())
			db.queue.remove({"url": n})
			print "En traitement", db.queue.count()
			print "Resultats", db.results.count()
			print "Erreur", db.log.count()
		if db.queue.count() == 0:
			break
	return "traitement terminé"

if __name__ == '__main__':
	liste = ["http://www.tourismebretagne.com/informations-pratiques/infos-environnement/algues-vertes"]
	query= "algues vertes OR algue verte"
	 
	print "ok"
	InitSeeds(liste, "db_test_crawtest_20")
	#Sourcing("db_test_crawtest_19")
	Crawler("db_test_crawtest_20", query)
	
