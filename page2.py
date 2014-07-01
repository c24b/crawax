from datetime import datetime
from filter import Filter

import requests
from random import choice
import BeautifulSoup as bs

class Page(object):
	def __init__(self, url):
		self.type = "defaut"
		self.url = url
		self.domain = ""
		self.crawl_date = self.start_date = datetime.now()
		self.unwanted_extensions = ['css','js','gif','asp', 'GIF','jpeg','JPEG','jpg','JPG','pdf','PDF','ico','ICO','png','PNG','dtd','DTD', 'mp4', 'mp3', 'mov', 'zip','bz2', 'gz', ]
		self.adblock = Filter(file('easylist.txt'))
	
	@property
	def logs(self):
		'''Check status values (error_msg, status_code, status)'''
		self.status = self.validate()
		self.status = self.request()
		self.status = self.filter()
		return {"url": self.url, "status":self.status, "code":self.status_code, "msg":self.error_msg, "date": self.start_date, "type":self.type}
	
	def validate(self):
		'''Bool: check the format of the next url compared to curr url'''
		if self.url is None or len(self.url) <= 1 or self.url == "\n":
			self.error_msg = "Url is empty"
			self.status_code = 204
			return False
			
		elif (( self.url.split('.')[-1] in self.unwanted_extensions ) and ( len( self.adblock.match(self.url) ) > 0 ) ):
			self.error_msg = "Url has not a proprer extension or page is an advertissement"
			self.status_code = 204
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
					self.raw_html = self.req.text
					self.status_code = 200
					self.error_msg = "Ok"
					return True
				except Exception, e:
					
					self.error_msg = "Request answer was not understood %s" %e
					self.status_code = 400
					return False
			except Exception, e:
				#print "Error requesting the url", e
				self.error_msg = "Request answer was not understood: %s" %e
				self.status_code = 400
				return False
		except requests.exceptions.MissingSchema:
			self.error_msg = "Incorrect url - Missing sheme for : %s" %self.url
			self.status_code = 406
			return False
		except Exception as e:
			self.error_msg = "Unknown exception: %s" %e
			self.status_code = 204
			return False
	
	def filter(self):
		'''Bool control the result if text/html or if content available'''
		#Content-type is not html 
		try:
			self.req.headers['content-type']
			if 'text/html' not in self.req.headers['content-type']:
				self.error_msg="Content type is not TEXT/HTML"
				self.status_code = 404
				return False
			#Error on ressource or on server
			elif self.req.status_code in range(400,520):
				self.status_code = self.req.status_code
				self.error_msg="Connexion error"
				return False
			#Redirect
			#~ elif len(self.req.history) > 0 | self.req.status_code in range(300,320): 
				#~ self.error_msg="Redirection"
				#~ self.bad_status()
				#~ return False
			else:
				self.status_code = 200
				self.msg = "Ok"
				return True	
		except Exception:
			self.error_msg="Request headers were not found"
			self.status_code = 403
			return False
	def extract(datatype_in, parser_type="beautifulSoup"):
		#~ def choose_parser_type(type):
			#~ if parser_type == "lxml":
				#~ self.parser = LxmlParser()
			#~ elif parser_type == "regex":
				#~ self.parser = RegexParser()
			#~ elif parser_type = "beautifulsoup":
				#~ self.parser = BeautiParser()
			#~ else:
				#~ raise NotImplementedError()
		if datatype_in == "article":			
			self.type = "article"
			self.title = bs(self.raw_html).title
			self.cleaned_text = re.sub("<.*?>", "", self.page["raw_html"])
			#meta
			self.meta_description = u""
			self.meta_lang = u""
			self.meta_favicon = u""
			self.meta_keywords = u""
			self.canonical_link = u""
			self.domain = u""
			#article
			self.top_node = None
			self.tags = set()
			#absolute link
			self.final_url = u""
			#article contextual extraction
			self.publish_date = None
			self.links = None
			self.outlinks = None
			self.backlinks = None
		else:
			pass
