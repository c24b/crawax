#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from database import Database, TASK_MANAGER_NAME, TASK_COLL
import re
from datetime import datetime
from abc import ABCMeta, abstractmethod
from page2 import Page
from validate_email import validate_email
import docopt
from utils import yes_or_no

class Scheduler(object):
	''' main access to Job Database'''
	def __init__(self):
		'''init the project base with db and collections'''
		self.task_db = Database(TASK_MANAGER_NAME)
		self.collection =self.task_db.create_coll(TASK_COLL)			
			
	def schedule(self, user_input):
		'''Schedule a new job from user_input (crawtext.py)'''
		j = Job.create_from_ui(user_input)
		if j is not False:
			#enter with single arg email
			if j['user'] is not None:
				#show all the project of the owner
				if self.select_job(j, "user") is None:
					print "User:%s is not already registered" %j["user"]
					print "To register you as user:\n1/ Create a new project: python crawtext.py mynewproject\n2/Set Ownership: python crawtext.py mynewproject -u you@cortext.net" %j["user"]
				else:
					self.select_job(j,"user")
				return 
			#enter with single project name					
			if j['name'] is not None and j['action'] is None: 	
				if j['name'] in ["crawl", "delete", "archive", "report", "export"]:
					print "**Project Name** can't be 'crawl', 'archive', 'report', 'export' or 'delete'"
					print "\t*To generate a report:\n\t\tcrawtext report pesticides"
					print "\t*To create an export :\n\t\tcrawtext export pesticides"
					print "\t*To delete a projet :\n\t\tcrawtext delete pesticides"
					return
				elif j['action'] is not None:
					if j['action'] == "delete":
						return self.delete({"name":j["name"]})
					
					elif j['action'] == "update":
						print j['update']
						existing_job = self.get_one({"name":j["name"],"action":"crawl"})				
						if existing_job is not None:
							for k,v in j.items():
								if v is not False and v is not None:
									existing_job[k] = v
							existing_job["date"].append(datetime.now())
							self.collection.update({"_id":existing_job["_id"]},existing_job, upsert=True) 
							print "Project %s successfully updated with new %s options !"%(j['name'], j['action'])
							return True
					else:
						self.collection.insert(j)
						print "Job %s has been successfully scheduled in project %s!"%(j['action'],j['name'])
						return True
				elif j['update'] is not None:
					print "Update"
					print j['update']
					existing_job = self.get_one({"name":j["name"]})				
					if existing_job is not None:
						for k,v in j.items():
							if v is not False and v is not None:
								existing_job[k] = v
						existing_job["date"].append(datetime.now())
						existing_job["action"] = "crawl"
						self.collection.update({"_id":existing_job["_id"]},existing_job, upsert=True) 
						print "Project %s successfully updated with new %s options !"%(j['name'], j['action'])
				else:
					if self.get_one({"name":j['name']}) is None:							
						print "No existing project found! "
						new = yes_no("Do you want to create a new CRAWL project with your parameters ?")
						if new == 1:
							j['action'] = "crawl"
							self.collection.insert(j)
							print "Project %s has been successfully created and set on %s! " %(j["name"], j["action"])
							return True
					#project exists
					else:
						if j['email'] is not None:
							print "Project %s will be owned by %s" %(j['name'], j['email'])
							for task in self.get_list({"name":j["name"]}):
								self.collection.update(task,{"$set":{"email": j["email"]}})
							return self.select_job(j, "email")
						else:
							return self.select_job({"name":j['name']})
				
		
	def delete(self, job_name):
		'''Delete existing project'''
		job_list = self.get_list(job_name)
		if job_list is not False:
			for n in job_list:
				self.collection.remove(n)
				print "Sucessfully deleted task:", n['name']
				
			print "All the tasks of the project %s have been sucessfully deleted !"%job_name['name']
			return True
		else:
			print "No existing project %s with active tasks found" %job_name['name']
			return False
			
	def get_one(self, project_name):
		if project_name is None:
			return None
		elif type(project_name) == dict:
			return self.collection.find_one(project_name)
		elif type(project_name) == str:
			if validate_email(project_name) is True:
				return self.collection.find_one({"email":job_name})
			else:	
				return self.collection.find_one({"name":job_name})
		else:
			return None
	
	def get_list(self, project_name=None):
		'''get all the current job'''		
		
		if project_name is None:
			return False
			#return [n["project"] for n in self.collection.distinct("name")]
		if type(project_name) == dict:
			project_list = [n for n in self.collection.find(project_name)]
			if len(project_list)> 0:
				#print "*** Project %s: %s ****" %(project_name.keys(), project_name.values())
				return project_list
			else:
				return  False
		else:
			return False
	
	def select_job(self, doc , by="name"):
		project_list = self.get_list({str(by): doc[str(by)]})
		if project_list is not False:
			print "***\tProject %s: %s\t***" %(str(by), str(doc[by]))
			for job in project_list:
				for k, v in job.items():
					if v is False or v is None:
						continue
					if k not in ['_id', by, '_key']:
						print "\t-", k,'\t', v
			return project_list
		else:
			return False
				
			
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
		'''Configure option of jobs'''
		job = {}
		job["action"] = None
		job["update"] = None
		#configure listing option if mail of owner or project_name
		if user_input['<name>'] is not None:
			
			if validate_email(user_input['<name>']) is True:
				job['user'] = user_input['<name>']
				job['email'] = user_input['<name>']
			else:
				job['name'] = user_input['<name>']				
				job["user"] = None
				job['email'] = None
			
			for k,v in user_input.items():
				k = re.sub("<|>|-|--", "", k)
				
				if k in ["report", "extract", "export", "delete", "archive", "crawl", "name"]:
					if v is True:
						job['action'] = k
						job["start_date"] = datetime.today()
				
				elif k in ["q", "s", "k"]:
					if v is True:
						print "Updating existing job %s"%(job["name"])
								
				elif k in ["set", "append", "expand", "delete", "query", "email", "file", "url"]:
					job[k] = v
					if v is not None:
						job["active"] = True
						job["date"] = [datetime.today()]
						job["configure"] = k
					if k == "email":
						if v is not None or False:
							job["user"] = v
							job["email"] = v
				elif k in ["user"]:
					if v is not None or False:
						job["user"] = v
				elif k in ["monthly", "weekly", "daily"]:
					if v is not None or False:
						job["frequency"] = v
					else:
						job["frequency"] = "monthly"
				else:		
					job[k] = v
			return job
		
		elif user_input['<url>'] is not None:
			print "Archiving %s" %user_input['<url>']
			raise NotImplementedError
		else:
			return False
		

	@staticmethod	
	def create_from_database(doc):
		'''doc.action = crawl ==> CrawlJob(doc)'''
		try:
			return globals()[(doc["action"]).capitalize()+"Job"](doc) 
		except KeyError:
			return NotImplementedError
	
				
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
class UpdateJob(Job):
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
