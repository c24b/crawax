#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from __future__ import print_function

from datetime import date
import requests
import re
from goose import Goose
from utils import Filter


class Page(object):
	def __init__(self):
		self.url = None
		self.raw_html = None
		self.crawl_date = None
		self.status = None
		self.error_type = None
		self.status_code = None
		self.type = "page"
		
class PageFactory():
	'''Page factory'''
	def __init__(self, url, query):
		self.url = url
		self.query = query
		self.page = Page()
		self.page.crawl_date = self.start_date = date.today()
		
		self.page.url = url
		self.page.query = query
		self.unwanted_extensions = ['css','js','gif','asp', 'GIF','jpeg','JPEG','jpg','JPG','pdf','PDF','ico','ICO','png','PNG','dtd','DTD', 'mp4', 'mp3', 'mov', 'zip','bz2', 'gz', ]	
		self.adblock = Filter(file('easylist.txt'))
	def create(self):	
		if self.check() and self.request() and self.control():
			if self.extract():
				return self.article
		else:
			return self.page

	def check(self):
		'''Bool: check the format of the next url compared to curr url'''
		if self.url is None or len(self.url) <= 1 or self.url == "\n":
			self.page.error_type = "Url is empty"
			self.page.status_code = 204
			self.page.status = False
			return False
		elif (( self.url.split('.')[-1] in self.unwanted_extensions ) and ( len( self.adblock.match(self.url) ) > 0 ) ):
			self.page.error_type="Url has not a proprer extension or page is an advertissement"
			self.page.status_code = 204
			self.page.status = False
			return False
		else:
			self.page.status = True
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
					
					self.page.raw_html = self.req.text
					self.page.status = True
					return True
				except Exception, e:
					
					self.page.error_type = "Request answer was not understood %s" %e
					self.page.status_code = 400
					self.page.status = False
					return False
				else:
					self.page.error_type = "Not relevant"
					self.page.status_code = 0
					self.page.status = True
					return False
			except Exception, e:
				#print "Error requesting the url", e
				self.page.error_type = "Request answer was not understood %s" %e
				self.page.status_code = 400
				self.page.status = False
				return False
		except requests.exceptions.MissingSchema:
			self.page.error_type = "Incorrect url - Missing sheme for : %s" %self.url
			self.page.status_code = 406
			self.page.status = False
			
			return False
		except Exception as e:
			self.page.error_type = "Another wired exception", e
			self.page.status_code = 204
			return False
		
	def control(self):
		'''Bool control the result if text/html or if content available'''
		#Content-type is not html 
		try:
			self.req.headers['content-type']
			if 'text/html' not in self.req.headers['content-type']:
				self.page.error_type="Content type is not TEXT/HTML"
				self.page.status_code = 404
				self.page.status = False
				return False
			#Error on ressource or on server
			elif self.req.status_code in range(400,520):
				self.page.status_code = self.req.status_code
				self.page.error_type="Connexion error"
				self.page.status = False
				return False
			#Redirect
			#~ elif len(self.req.history) > 0 | self.req.status_code in range(300,320): 
				#~ self.error_type="Redirection"
				#~ self.bad_status()
				#~ return False
			else:
				self.page.status_code = 200
				self.page.status = True
				return True	
		except Exception:
			self.page.error_type="Request headers are not found"
			self.page.status_code = 403
			self.page.status = False
			return False		
		
	def extract(self):
		'''Dict extract content and info of webpage return boolean and self.info'''
		
		try:
			#using Goose extractor
			#print "extracting..."
			self.article = ArticleFactory(raw_html=self.page.raw_html, url=self.page.url)
			self.article.extract()
			#self.article = Goose(raw_html=self.page.raw_html, url=self.page.url)
			
			#filtering relevant webpages
			
			if self.filter() is True:
				self.type = "article"
				#self.article.outlinks = set([self.clean_url(url=e.attrs['href']) for e in bs(self.src).find_all('a', {'href': True})])
				#print self.outlinks

				# self.info = {	
				# 				"url":self.url,
				# 				"query": self.query,
				# 				"domain": get_tld(self.url),
				# 				"outlinks": [{"url":n, "domain":get_tld(n)} for n in self.outlinks if n is not None],
				# 				"backlinks":[{"url":n, "domain":get_tld(n)} for n in self.outlinks if n == self.url],
				# 				"texte": self.article.cleaned_text,
				# 				"title": self.article.title,
				# 				"meta_description":bs(self.article.meta_description).text,
				# 				"date": [self.crawl_date]
				# 				}
				return self.article
			else:
				self.page.error_type = "Not relevant"
				self.page.status_code = 0
				self.page.status = True
				return self.page	
		except Exception, e:
			#print e
			self.page.error_type = str(e)
			self.page.status_code = -1
			self.page.status = False
			return self.page		
	
	def filter(self):
		#to
		'''Bool Decide if page is relevant and match the correct query. Reformat the query properly: supports AND, OR and space'''
		if self.article.cleaned_text is not None or self.article.cleaned_text != '':
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
		else:
			return False	 	
	def bad_status(self):
		'''create a msg_log {"url":self.url, "error_code": self.req.status_code, "error_type": self.error_type, "status": False,"date": self.crawl_date}'''			
		try:
		 	return {"url":self.page.url, "query": self.query, "error_code": str(self.req), "type": self.page.error_type, "status": False, "date":[self.page.crawl_date]}
		except:
		 	return {"url":self.url, "query": self.query, "error_code": "No request answer", "type": self.error_type, "status": False, "date":[self.crawl_date]}
	
	