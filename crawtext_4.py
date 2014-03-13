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
from pymongo import Connection
from pymongo.errors import ConnectionFailure
from pymongo import errors
from bs4 import BeautifulSoup as bs
from urlparse import urlparse
from random import choice
from goose import Goose

import __future__


unwanted_extensions = ['css','js','gif','asp', 'GIF','jpeg','JPEG','jpg','JPG','pdf','PDF','ico','ICO','png','PNG','dtd','DTD', 'mp4', 'mp3', 'mov', 'zip','bz2', 'gz', ]	
class Database(object):
	def __init__(self, name="full_test", host="localhost", port=27017):
		self.db_name = name
		self.host = host
		self.port = port		
		print "Database is ", self.db_name
		self.connect()
	
	def connect(self):
		'''Connect to MongoDb'''
		try:
			c = Connection(self.host, self.port)
		except	ConnectionFailure,e:
			sys.stderr.write("Could not connect to MongoDB: %s" % e)
			sys.exit(1)
		self.db = c.name
		return self.db
			
	def create_tables(self):
		'''Creating tables'''
		self.results = self.db['results']
		self.queue = self.db['queue'] 
		self.report = self.db['report']
		return self
		
class Page(object):
	def __init__(self, url, query):
		self.url = url
		self.query = query
		self.db = db
		#properties
		self.title = None
		self.description = None
		self.content = None
		#self.soup = None
		self.outlinks = []
		self.backlinks = []
		self.status = None
		self.error_type = None
		
	def bad_status(self):
		self.status = False
		try:
			self.error = {"url":self.url, "error_code": self.req.status_code, "type": self.error_type, "status": False}
		except AttributeError:
			self.error = {"url":self.url, "error_code": 404, "type": self.error_type, "status": False}
		return

	def pre_check(self):
		if (( self.url.split('.')[-1] in unwanted_extensions ) and ( len( adblock.match(self.url) ) > 0 ) ):
				self.error_type="Url has not a proprer extension or page is an advertissement"
				self.bad_status()
				return False
		else:
			self.status = True
			return True
		
	def check(self):		
		if 'text/html' not in self.req.headers['content-type']:
			self.error_type="Content type is not TEXT/HTML"
			self.bad_status()
			return False
		#Error on ressource or on server
		elif self.req.status_code in range(400,520):
			self.error_type="Connexion error"
			self.bad_status()
			return False
		#Redirect
		elif len(self.req.history) > 0 | self.req.status_code in range(300,320): 
			self.error_type="Redirection"
			self.bad_status()
			return False
		else:
			return True	
	
	def request(self):
		print "connect to", self.url
		try:
			requests.adapters.DEFAULT_RETRIES = 2
			user_agents = [u'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1', u'Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2', u'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0', u'Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00']
			headers = {'User-Agent': choice(user_agents),}
			proxies = {"https":"77.120.126.35:3128", "https":'88.165.134.24:3128', }
			self.req = requests.get((self.url), headers = headers,allow_redirects=True, proxies=proxies, timeout=5)
			print self.req.status_code
			if self.pre_check() and self.check():
				try:
					self.src = self.req.text
						
				except Exception, e:
					self.error_type = "Request answer was not understood %s" %e
					self.bad_status()
				
			else:
				self.error_type = "Not relevant"
				self.bad_status()
			
		
		except requests.exceptions.MissingSchema:
			self.error_type = "Incorrect url %s" %self.url
			self.bad_status()
		return self
	def extract(self):
		try:
			self.soup = bs(self.src)
			g = Goose()
			article = g.extract(raw_html=self.src)
			self.title = article.title
			self.text = article.cleaned_text
			self.description = bs(article.meta_description).text
		except Exception, e:
			self.error_type = str(e)
			self.bad_status()
		return self
	
	def get(self):
		self.result = {}
		_inherited = ["status", "description", "text","outlinks","backlinks","url","title"]
		for name in self.__dict__:
			if name in _inherited:
				self.result.update({name :self.__dict__[name]})
		return self.result
				
	def clean_url(self, url):
		self.netloc = 'http://' + urlparse(self.url)[1]
		if url not in [ '#', None, '\n', '' ] and 'javascript' not in url:
			if urlparse(url)[1] == '':
				if url[0] == '/':
					url = self.netloc + url
				else:
					url = self.netloc + '/' + url
			elif urlparse(url)[0] == '':
				url = 'http:' + url
			return url
	
	def next_step(self):
		from multiprocessing import Pool
		if self.status is True:
			p = Pool(5)
			self.outlinks = list(set([self.clean_url(e.attrs['href']) for e in self.soup.find_all('a', {'href': True}) if self.clean_url(e.attrs['href']) is not None]))
			self.backlink = list(set([n for n in self.outlinks if n == self.url]))
			return self.outlinks
		
				
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
			 	
		
	def store(self):
		results = self.__dict__	
		return self.__dict__
	
		
if __name__ == '__main__':
	liste = ["http://www.tourismebretagne.com/informations-pratiques/infos-environnement/algues-vertes","http://www.developpement-durable.gouv.fr/Que-sont-les-algues-vertes-Comment.html", "test.com"]
	query= "algues vertes OR algue verte"
	db = Database("test_crawltext_4")
	db.create_tables()
	for n in liste:
		p = Page(n, query)
		
		p.request()
		p.extract()
		p.next_step()
		result = p.get()
		
		if p.status is False:
			print p.error
		else:
			print result['title']
