#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from __future__ import print_function

import datetime
from os.path import exists
import sys
import requests
import json
import re
from goose import Goose
from pymongo import errors as mongo_err
from bs4 import BeautifulSoup as bs
from urlparse import urlparse
from random import choice
from tld import get_tld
from abpy import Filter


unwanted_extensions = ['css','js','gif','asp', 'GIF','jpeg','JPEG','jpg','JPG','pdf','PDF','ico','ICO','png','PNG','dtd','DTD', 'mp4', 'mp3', 'mov', 'zip','bz2', 'gz', ]	
adblock = Filter(file('easylist.txt'))

class Page():
	'''Page factory'''
	def __init__(self, url, query):
		self.url = url
		self.query = query
		self.status = None
		self.error_type = "Ok"
		self.info = {}
		self.crawl_date = datetime.datetime.now()
		self.req = None
		self.src = ""
		self.status_code = 0
		
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
			try:
				self.req = requests.get((self.url), headers = headers,allow_redirects=True, proxies=None, timeout=5)
				
				try:
					
					self.src = self.req.text
					return True
				except Exception, e:
					
					self.error_type = "Request answer was not understood %s" %e
					self.status_code = 400
					return False
				else:
					self.error_type = "Not relevant"
					self.status_code = 0
					return False
			except Exception, e:
				#print "Error requesting the url", e
				self.error_type = "Request answer was not understood %s" %e
				self.status_code = 400
				return False
		except requests.exceptions.MissingSchema:
			self.error_type = "Incorrect url - Missing sheme for : %s" %self.url
			self.status_code = 406
			
			return False
		except Exception as e:
			self.error_type = "Another wired exception", e
			self.status_code = 204
			return False
		
	def control(self):
		'''Bool control the result if text/html or if content available'''
		#Content-type is not html 
		try:
			self.req.headers['content-type']
			if 'text/html' not in self.req.headers['content-type']:
				self.error_type="Content type is not TEXT/HTML"
				self.status_code = 404
				return False
			#Error on ressource or on server
			elif self.req.status_code in range(400,520):
				self.status_code = self.req.status_code
				self.error_type="Connexion error"
				return False
			#Redirect
			#~ elif len(self.req.history) > 0 | self.req.status_code in range(300,320): 
				#~ self.error_type="Redirection"
				#~ self.bad_status()
				#~ return False
			else:
				self.status_code = 200
				self.error_type= "Ok"
				return True	
		except Exception:
			self.error_type="Request headers are not found"
			self.status_code = 403
			return False		
		
	def extract(self):
		'''Dict extract content and info of webpage return boolean and self.info'''
		
		try:
			#using Goose extractor
			#print "extracting..."
			g = Goose()
			self.article = g.extract(raw_html=self.src)
			#filtering relevant webpages
			
			if self.filter() is True:
				self.outlinks = set([self.clean_url(url=e.attrs['href']) for e in bs(self.src).find_all('a', {'href': True})])
				#print self.outlinks
				self.info = {	
								"url":self.url,
								"query": self.query,
								"domain": get_tld(self.url),
								"outlinks": list(self.outlinks),
								"backlinks":[n for n in self.outlinks if n == self.url],
								"texte": self.article.cleaned_text,
								"title": self.article.title,
								"meta_description":bs(self.article.meta_description).text,
								"date": [self.crawl_date]
								}
				return self.info
			else:
				self.error_type = "Not relevant"
				self.status_code = 0
				return False	
		except Exception, e:
			print e
			self.error_type = str(e)
			self.status_code = -1
					
	def filter(self):
		'''Bool Decide if page is relevant and match the correct query. Reformat the query properly: supports AND, OR and space'''
		self.query = re.sub('-', ' ', self.query) 
		if 'OR' in self.query:
			for each in self.query.split('OR'):
				query4re = each.lower().replace(' ', '.*')
				if re.search(query4re, self.article.cleaned_text, re.IGNORECASE) or re.search(query4re, self.url, re.IGNORECASE):
					return True

		elif 'AND' in self.query:
			query4re = self.query.lower().replace(' AND ', '.*').replace(' ', '.*')
			return bool(re.search(query4re, self.article.cleaned_text, re.IGNORECASE) or re.search(query4re, self.url, re.IGNORECASE))
		#here add NOT operator
		else:
			query4re = self.query.lower().replace(' ', '.*')
			return bool(re.search(query4re, self.article.cleaned_text, re.IGNORECASE) or re.search(query4re, self.url, re.IGNORECASE))
			 	
	def bad_status(self):
		'''create a msg_log {"url":self.url, "error_code": self.req.status_code, "error_type": self.error_type, "status": False,"date": self.crawl_date}'''			
		try:
		 	return {"url":self.url, "query": self.query, "error_code": str(self.req), "type": self.error_type, "status": False, "date":[self.crawl_date]}
		except:
		 	return {"url":self.url, "query": self.query, "error_code": "No request answer", "type": self.error_type, "status": False, "date":[self.crawl_date]}
	
	def clean_url(self, url):
		''' utility to normalize url and discard unwanted extension : return a url or None'''
		#ref tld: http://mxr.mozilla.org/mozilla-central/source/netwerk/dns/effective_tld_names.dat?raw=1
		#if url in ["#"]:
		#	print url
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
