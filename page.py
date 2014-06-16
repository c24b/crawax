#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from __future__ import print_function

from datetime import date
import requests
import re
#from goose import Goose
from utils import Filter
from random import choice
from article import Article

class Page(object):
	def __init__(self, url, query):
		self.url = None
		self.raw_html = None
		self.crawl_date = None
		self.status = None
		self.error_type = None
		self.status_code = None
		self.type = "page"

		self.url = url
		self.query = query
		
		self.crawl_date = self.start_date = date.today()

		self.unwanted_extensions = ['css','js','gif','asp', 'GIF','jpeg','JPEG','jpg','JPG','pdf','PDF','ico','ICO','png','PNG','dtd','DTD', 'mp4', 'mp3', 'mov', 'zip','bz2', 'gz', ]	
		self.adblock = Filter(file('easylist.txt'))
		self.create()

	def create(self):	
		if self.check() and self.request() and self.control():
			return Article()
		else:
			return self.bad_status()

	def check(self):
		'''Bool: check the format of the next url compared to curr url'''
		if self.url is None or len(self.url) <= 1 or self.url == "\n":
			self.error_type = "Url is empty"
			self.status_code = 204
			self.status = False
			return False
		elif (( self.url.split('.')[-1] in self.unwanted_extensions ) and ( len( self.adblock.match(self.url) ) > 0 ) ):
			self.error_type="Url has not a proprer extension or page is an advertissement"
			self.status_code = 204
			self.status = False
			return False
		else:
			self.status = True
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
					
					self.raw_html = self.req.text
					self.status = True
					return True
				except Exception, e:
					
					self.error_type = "Request answer was not understood %s" %e
					self.status_code = 400
					self.status = False
					return False
				else:
					self.error_type = "Not relevant"
					self.status_code = 0
					self.status = True
					return False
			except Exception, e:
				#print "Error requesting the url", e
				self.error_type = "Request answer was not understood %s" %e
				self.status_code = 400
				self.status = False
				return False
		except requests.exceptions.MissingSchema:
			self.error_type = "Incorrect url - Missing sheme for : %s" %self.url
			self.status_code = 406
			self.status = False
			
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
				self.status = False
				return False
			#Error on ressource or on server
			elif self.req.status_code in range(400,520):
				self.status_code = self.req.status_code
				self.error_type="Connexion error"
				self.status = False
				return False
			#Redirect
			#~ elif len(self.req.history) > 0 | self.req.status_code in range(300,320): 
				#~ self.error_type="Redirection"
				#~ self.bad_status()
				#~ return False
			else:
				self.status_code = 200
				self.status = True
				return True	
		except Exception:
			self.error_type="Request headers are not found"
			self.status_code = 403
			self.status = False
			return False

	def bad_status(self):
		'''create a msg_log {"url":self.url, "error_code": self.req.status_code, "error_type": self.error_type, "status": False,"date": self.crawl_date}'''			
		try:
			return {"url":self.url, "query": self.query, "error_code": self.status_code, "type": self.error_type, "status": False, "date":[self.page.crawl_date]}
		except:
			return {"url":self.url, "query": self.query, "error_code": "No request answer", "type": self.error_type, "status": False, "date":[self.crawl_date]}
	
	