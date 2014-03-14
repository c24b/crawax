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

import __future__


unwanted_extensions = ['css','js','gif','asp', 'GIF','jpeg','JPEG','jpg','JPG','pdf','PDF','ico','ICO','png','PNG','dtd','DTD', 'mp4', 'mp3', 'mov', 'zip','bz2', 'gz', ]	


class Database():
	def __init__(self, database_name):
		self.name = database_name
		client = MongoClient('mongodb://localhost,localhost:27018')
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
		self.db = db
		self.status = None
		
	def bad_status(self):
		self.status = False
		try:
			self.log = {"url":self.url, "error_code": self.req.status_code, "type": self.error_type, "status": False}
		except AttributeError:
			self.log= {"url":self.url, "error_code": 404, "type": self.error_type, "status": False}
		return self.log
		 	
	def pre_check(self):
		if (( self.url.split('.')[-1] in unwanted_extensions ) and ( len( adblock.match(self.url) ) > 0 ) ):
				self.error_type="Url has not a proprer extension or page is an advertissement"
				print self.error_type
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
		print self.url
		if self.pre_check() is True:
			
			#self.url = self.clean_url(self.url)
			try:
				requests.adapters.DEFAULT_RETRIES = 2
				user_agents = [u'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1', u'Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2', u'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0', u'Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00']
				headers = {'User-Agent': choice(user_agents),}
				proxies = {"https":"77.120.126.35:3128", "https":'88.165.134.24:3128', }
				self.req = requests.get((self.url), headers = headers,allow_redirects=True, proxies=proxies, timeout=5)
				if self.pre_check() and self.check():
					try:
						self.src = self.req.text
						return True	
					except Exception, e:
						self.error_type = "Request answer was not understood %s" %e
						self.bad_status()
						return False
				else:
					self.error_type = "Not relevant"
					self.bad_status()
					return False
			
			except requests.exceptions.MissingSchema:
				self.error_type = "Incorrect url %s" %self.url
				self.bad_status()
				return False
				
		
	def extract(self):
		try:
			self.soup = bs(self.src)
			g = Goose()
			article = g.extract(raw_html=self.src)
			self.title = article.title
			self.text = article.cleaned_text
			self.description = bs(article.meta_description).text
			return True
		except Exception, e:
			self.error_type = str(e)
			self.bad_status()
			return False
	
	
				
	def clean_url(self, url):
		#http://mxr.mozilla.org/mozilla-central/source/netwerk/dns/effective_tld_names.dat?raw=1
		uid = urlparse(self.url)
		if uid.netloc == "":
			print uid
		#~ if re.split("\.", uid.netloc)[0] != 'www':
			#~ url = 
		#~ self.netloc = 'http://' + uid[1]
		#~ if url not in [ '#', None, '\n', '' ] and 'javascript' not in url:
			#~ if uid[1] == '':
				#~ if url[0] == '/':
					#~ url = self.netloc + url
				#~ else:
					#~ url = self.netloc + '/' + url
			#~ elif uid[0] == '':
				#~ url = 'http:' + url
			#~ return url
	
	def next_step(self):
		if self.status is True:	
			self.outlinks = list(set([self.clean_url(e.attrs['href']) for e in self.soup.find_all('a', {'href': True}) if self.clean_url(e.attrs['href']) is not None]))
			self.backlinks = list(set([n for n in self.outlinks if n == self.url]))
		return self.status
			
		
				
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
			 	
		
	def getter(self):
		try:
			self.info = {	
						"url":self.url,
						"outlinks": self.outlinks,
						"backlinks":self.backlinks
						}
							
			return True
		except AttributeError, e:
			self.status = False
			self.error_type = str(e.args)
			self.bad_status()
			return False
		
if __name__ == '__main__':
	liste = ["http://www.tourismebretagne.com/informations-pratiques/infos-environnement/algues-vertes","http://www.developpement-durable.gouv.fr/Que-sont-les-algues-vertes-Comment.html"]
	query= "algues vertes OR algue verte"
	db = Database("test_crawltext_7")
	db.create_tables()
	for n in liste:
		
		print n
		p = Page(n, query)
		if p.request() and p.extract() and p.next_step() and p.getter():
			db.results.insert(p.info)
			
			db.queue.insert([{"url":url} for url in p.outlinks])
			
			
	while db.queue.distinct("url") != 0:
		for n in db.queue.distinct("url"):
			p = Page(n, query)
			if p.request() and p.extract() and p.next_step() and p.getter():
				db.results.insert(p.info)
				db.queue.insert([{"url":url} for url in p.outlinks])
			db.queue.remove({"url": n})
