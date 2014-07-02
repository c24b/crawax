#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database import Database, TASK_MANAGER_NAME, TASK_COLL
import re
from datetime import datetime
from abc import ABCMeta, abstractmethod
from page2 import Page
from validate_email import validate_email
import docopt

class Scheduler(object):
	''' main access to Job Database'''
	def __init__(self):
		'''init the project base with db and collections'''
		self.task_db = Database(TASK_MANAGER_NAME)
		self.collection =self.task_db.create_coll(TASK_COLL)	
		
			
	def schedule(self, user_input):
		'''Schedule a new job from user_input (crawtext.py)'''
		j = Job.create_from_ui(user_input)
		if j['action'] == "configure":
			for k,v in j.items():
				if k != "name" or k != "action":
					self.collection.update({"name":j['name']},{"$set":{"action":"crawl"}}, True)
					self.collection.insert({"name":j['name']},{"$set":{k:v}}, False)
					
			print "%s has been sucessfully updated!"%j['name']
			return
			#self.collection.update({"name":j['name'], "action":"crawl"}, j, False)
		if j['action'] == "create":
			if len([n for n in self.collection.find({"name":j['name']})]) > 0:
				print "Project", j["name"]
				for n in self.collection.find({"name":j['name']}):
					print "-", n["action"], n["user"]
					return
			else:
				self.collection.insert(j,True)
				self.collection.update({"name":j['name'], "action":"create"}, {"$set":{"action":"crawl"}},False)
				print "%s has been sucessfully created with a defaut crawl configuration!"%j['name']
				return
		else:	
			if j['action'] != "archive":
				if j['action'] == "delete":
					self.collection.remove({"name":j['name']})
					print "%s has been sucessfully deleted !"%j['name']
				else:
					if len([n for n in self.collection.find({"name":j['name'], "action":"crawl"})]) > 0:
						self.collection.insert(j,True)
						print "%s has been sucessfully programmed !"%j['name']
					else:
						print "%s has no initial crawl to proceed to operation"%j['name']
						print ">To create a initial crawl project:\n\tcrawtext.py %s"%j['name']
			return 
	
	
	def delete(self, job_name):
		'''Delete existing job using name'''
		for n in self.get_list():
			if n["name"] == job_name:
				self.collection.remove({"name": n["name"]})
				print "Sucessfully deleted task:", job_name
			else:
				continue
				
	def get_one(self, job_name):
		'''get the current job from DB using Job'''
		return  self.collection.find_one({"name":job_name})
		
	def get_project(self, job_name, action_type=None):
		'''get the current job by name and type of job'''
		if action_type is not None:
			return  self.collection.find_one({"name":job_name, "action":action_type})
		else:
			return  self.collection.find_one({"name":job_name, "action":action_type})
			
	def get_projects(self, job_name, action_type=None):
		'''get every jobs that has the same name'''
		if action_type is not None:
			return  [n for n in self.collection.find({"name":job_name, "action":action_type})]
		else:
			return  [n for n in self.collection.find({"name":job_name})]
		
	def get_owner(self, email):
		'''get all the jobs for one user'''
		return  [n for n in self.collection.find({"email":email})]
	
	def get_list(self, project_name=None):
		'''get all the current job'''
		if project_name is not None:
			return  [n for n in self.collection.find({"name":project_name})]
		else:
			return [n for n in self.collection.find()]
	
	def get_project_list(self, project_name):
		#self.aggregate(project_name)
		'''get all the current jobs for one project base on project name'''
		return [n for n in self.specific_coll.find()]
				
	def run_job(self, job_name=None):
		'''Execute tasks from Job Database'''
		if job_name is not None:
			doc = self.get_one(job_name)		
			j = Job.create_from_database(doc)
			print "Running %s on %s" %(j.name, j.action)
			return j.run()
		else:
			docs = self.get_list()
			for doc in docs:
				j = Job.create_from_database(doc)
				print "Running %s on %s" %(j.name, j.action)
				j.run()
			return "All jobs done !"
		
class Job(object):
	__metaclass__ = ABCMeta
		
	@staticmethod	
	def create_from_ui(user_input):
		'''Send new job into Task Manager DB'''
		job = {}
		if user_input['<name>'] is not None:
			
			if user_input['<name>'] in ['archive', 'report', 'export', 'delete']:
				print "**Project Name** can't be 'archive', 'report', 'export' or 'delete'"
				print ">To create or consult a project:\n\tcrawtext.py pesticides"
				print ">For other option specify the project name:" 
				print "\t*To generate a report:\n\t\tcrawtext report pesticides"
				print "\t*To create an export :\n\t\tcrawtext export pesticides"
				print "\t*To delete a projet :\n\t\tcrawtext delete pesticides"
				print ">For archiving please specify the url:" 
				print "\t*To archive a website :\n\t\tcrawtext archives www.lemonde.fr"
				return False
			else:
				#Get project_name
				if validate_email(user_input['<user>']) is True:
					job['user'] = user_input['<user>']
					job['name'] = None
				else:
					job['name'] = user_input['<user>']
					job['user'] = None
					job['action'] = "create"
					job['date'] = datetime.now()
					job['active'] = True
					job['recurrence'] = 'monthly'
				
		#print dict_values
		for k,v in user_input.items():
			if v is not None and v is not False:
				k = re.sub("<|>|-|--", "", k)
				if k in ["report", "extract", "export", "delete", "archive"]:
					job['action'] = k
				elif k in ["query", "email", "url", "key", "file"]:
					job["action"] = "configure"
					job[k] = v
					job["active"] = True
				elif k in ["monthly", "weekly", "daily"]:
					job["frequency"] = v
				else:
					job[k] = v
					
		job["date"] = datetime.today()
		job["user"] = None	
		return job

	@staticmethod	
	def create_from_database(doc):
		'''doc.action = crawl ==> CrawlJob(doc)'''
		return globals()[(doc["action"]).capitalize()+"Job"](doc) 
		
		
	def __repr__(self):
		'''print Job properties'''
		return self.__dict__	
			    
		
	def run(self):
		print "running Job..."
		pass
		
class CrawlJob(Job):
	def __init__(self, doc): 
		self.date = datetime.now()
		for k, v in doc.items():
			setattr(self,k,v) 	
		self.db = Database(self.name)
		self.db.create_colls()	
	
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
				self.insert_url(e["Url"],origin="bing")
			return True
		except Exception as e:
			print e
			self.status_code = -1
			self.error_type = "Error fetching results from BING API.\nError is : (%s).\n>>>>Check your credentials: number of calls may not exceed 5000req/month" %e.args
			return False

	def get_local(self):
		''' Method to extract url list from text file'''
		try:
			for url in open(self.file).readlines():
				url = re.sub("\n", "", url)
				self.insert_url(url, origin=self.file)
			return True
		except Exception:
			self.status_code = -1
			self.error_type = "Error fetching results from file: %s.\n>>> Check if file exists" %self.file
			print self.error_type
			return False
	def expand(self):
		'''Expand sources url adding results urls collected from previous crawl'''
		for url in self.db.results.distinct("url"):
			if url not in self.db.sources.find({"url": url}):
				self.insert_url(url, origin="expand")
		return
				
	def insert_url(self, url, origin="default"):
		if url not in self.db.sources.find({"url": url}):
			self.db.sources.insert({"url":url, "origin":"bing","date":[datetime.today()]}, upsert=False)
		else:
			self.db.sources.update({"url":url,"$push": {"date":datetime.today()}}, upsert=True)
		return self.db.sources.find_one({"url": url})
		
	def collect_sources(self):
		''' Method to add new seed to sources and send them to queue if sourcing is deactivate'''
		if self.file is not None:
			self.get_local()
		if self.query is not None and self.key is not None:
			self.get_bing()
		#~ if self.expand is True:
			#~ self.expand()
		return self
		
	def send_seeds_to_queue(self):
		#here we could filter out problematic urls
		for url in self.db.sources.distinct("url"):
			self.db.queue.insert({"url":url})
		return self
		
	def activate(self):
		try:
			#if self.sourcing is False:
			self.collect_sources()
		except AttributeError:
			pass
		return self.send_seeds_to_queue()
		
	def run(self):
		print "Running crawler..."
		self.activate()
		start = datetime.now()
		while self.db.queue.count > 0:
			for url in self.db.queue.distinct("url"):
				page = Page(url)
				if page.logs["status"] is False:
					self.db.logs.insert(page.logs)
				else:
					page.extract("article")
					print page.title 
					
				#~ print page.status
					#print page.canonical_link
				# else:
				# 	self.db.logs.insert(article.bad_status())
				self.db.queue.remove({"url": url})
				if self.db.queue.count() == 0:
					break
			
			if self.db.queue.count() == 0:		
				break
		
		end = datetime.now()
		elapsed = end - start
		print "crawl finished in %s" %(elapsed)
		print self.db.stats()
		return 
	
class ReportJob(Job):
	def __init__(self, doc):
		self.date = datetime.now()
		for k, v in doc.items():
			setattr(self,k,v) 	
		self.db = Database(self.name)
		
	def run(self):
		print "Report:"
		filename = "Report_%s_%d" %(self.name, self.date)
		with open( 'a') as f:
			f.write((self.db.stats()).encode('utf-8'))
		print "Successfully generated report for %s" %self.name 	
		return self	
		
class ExtractJob(Job):
	def __init__(self, doc):
		self.date = datetime.now()
		for k, v in doc.items():
			setattr(self,k,v) 	
		pass
class ExportJob(Job):
	def __init__(self, doc):
		self.date = datetime.now()
		for k, v in doc.items():
			setattr(self,k,v) 	
		pass
class RunJob(Job):
	def __init__(self, doc):
		self.date = datetime.now()
		for k, v in doc.items():
			setattr(self,k,v) 	
		pass

class DeleteJob(Job):
	def __init__(self, doc):
		self.date = datetime.now()
		for k, v in doc.items():
			setattr(self,k,v) 	
		pass
