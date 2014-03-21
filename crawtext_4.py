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
		self.db = db
		self.status = None
		if url is None or url == "":
			self.status = False
		self.domain = None
	def do_page(self, url, query):
		self.pre_check(url)
		self.request()
		self.check()
		self.extract()


	def bad_status(self):
		'''create a msg_log {"url":self.url, "error_code": self.req.status_code, "type": self.error_type, "status": False}'''
		self.msg_log = None
		try:
			self.msg_log = {"url":self.url, "error_code": self.req.status_code, "type": self.error_type, "status": False}
		except AttributeError:
			try:
				self.msg_log = {"url":self.url, "error_code": "Undefined", "type": self.error_type, "status": False}
		 	except AttributeError:
				pass
		return self.msg_log
				
	def pre_check(self, url=None):
		''' check the format of the next url compared to curr url : boolean answer'''
		#curr url is self.url
		#next url is url
		
		#current link
		if self.url is not None or len(self.url) > 1 or self.url == "\n":
			self.curr = urlparse(self.url)
			if (( self.url.split('.')[-1] in unwanted_extensions ) and ( len( adblock.match(self.url) ) > 0 ) ):
				self.error_type="Url has not a proprer extension or page is an advertissement"
				return False
			else:
				if url is not None:
					self.next = urlparse(self.url)
					if self.next.netloc == '' or len(self.next.netloc) <=1 or self.next.netloc is None:
						return False
					else:	
						print "Urlparse", self.next.netloc
						return True
		else:
			return False	
		#~ try:
		#~ except Exception, e:
			#~ self.error_type="Not a valid url and domain name"
			#~ self.status = False
			#~ return False
		
	def check(self):
		'''control the result of request return a boolean '''
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
		
	def request(self):
		'''request a webpage: return boolean'''
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
		
	def extract(self):
		'''extract content and info of webpage return boolean'''
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
			return False
		
				
	def clean_url(self, url):
		''' utility to normalize url and discard unwanted extension : return a url'''
		#ref tld: http://mxr.mozilla.org/mozilla-central/source/netwerk/dns/effective_tld_names.dat?raw=1
		clean_url = None
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
		
	def next_step(self):
		'''return a list of outlinks and backlinks'''
		self.outlinks = [self.clean_url(url=e.attrs['href']) for e in self.soup.find_all('a', {'href': True})]
		self.backlinks = [n for n in self.outlinks if n == self.url]	
		return self
				
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
						"source": self.domain,
						"url":self.url,
						"outlinks": self.outlinks,
						"backlinks":self.backlinks,
						"texte": self.text,
						"title": self.title
						}
							
			return True
		except AttributeError, e:
			print e
			self.status = False
			self.error_type = str(e.args)
			return False
		
if __name__ == '__main__':
	liste = ["http://www.tourismebretagne.com/informations-pratiques/infos-environnement/algues-vertes","http://www.developpement-durable.gouv.fr/Que-sont-les-algues-vertes-Comment.html"]
	query= "algues vertes OR algue verte"
	db = Database("test_crawltext_13")
	db.create_tables()
	
	#constitution de la base
	for n in liste:
		print n
		p = Page(n, query)
		if (p.request() and p.extract() and p.next_step() and p.getter()) is True:
			db.results.insert(p.info)
			db.sources.insert({"url":p.info["url"]})
			print p.outlinks
			db.queue.insert([{"url":url} for url in p.outlinks])
		else:
			print p.request(), p.extract(), p.next_step(), p.getter()
			print p.bad_status()
			db.log.insert(p.msg_log)
					
	print "Nb de sources", db.sources.count()
	print "Nb urls en traitement", db.queue.count()
	print "nb erreur", db.log.count()
	while db.queue.count > 0:
		for n in db.queue.distinct("url"):	
			p = Page(n, query)
			if p.request() and p.extract() and p.next_step() and p.getter():
				#print p.info["title"]
				if (p.info["texte"] not in db.queue.find({"texte": p.info["texte"]})):
					db.results.insert(p.info)
					db.queue.insert([{"url":url} for url in p.outlinks])
			else:
				p.bad_status()
				if p.msg_log is not None:
					db.log.insert(p.msg_log)
			db.queue.remove({"url": n})
	

