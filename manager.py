#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
manager.py
Utils to send CRON jobs with a mongodb collection 
that stores project and initial configuration given by user 
using crawtext script

"""
from datetime import datetime, date
import requests
import re
import json
from database import Database
from multiprocessing import Pool
from crawler import crawler

MANAGER = "Manager"
JOBS = "Jobs"
TASK_MANAGER_NAME = "manager"

class Manager():
	'''Simple task manager with info sent by user using crawtext or acessing scheduled jobs'''
	def __init__(self, docopt_args=None):
		'''Initializing projet with parameters stored in a projet database AND user input'''
		#Load the Taskmanager database
		self.task_db = Database(TASK_MANAGER_NAME)
		self.collection =self.task_db.create_coll('tasks')	
		
		if docopt_args is None:
			'''run every jobs in task manager'''
			print "running every jobs in Manager"
			self.run()

		elif type(docopt_args) == str:
			'''manage an existing job'''
			print "running crawl for %s" %docopt_args
			self.run_job(docopt_args)
			# self.project = docopt_args
			# self.find()
			# self.manage_job()
		
		elif type(docopt_args) != str:
			'''configure a job with crawtext docopt'''
			#Load user input as attributes of Manager
			print "Configuring job %s" %docopt_args
			self.configure_job(docopt_args)
			# self.config(docopt_args)
			# self.dispatch()
		
		
		else:
			print "Not Implemented"
			pass
	
	def run(self):
		'''manage every jobs in task manager'''
		today = date.today()
		for n in self.collection.find():
			self.name = n["project"]
			job = Job(self.name)
			job.run()
			job.update()
		return 
	def run_job(self, docopt_args):
		j = Job(docopt_args)
		j.find_job()
		j.run()
		return j.update()
	def find_job(self, docopt_args):
		self.
		self.doc = self.collection.find():	


	def configure_job():
		if self.find_job():
			"print updating existing job with last options"
			return self.update_job()
		else:
			return self.create_job()


	def config(self, docopt_args):
		'''Mapping user parameters into object attributes'''
		for k, v in docopt_args.items():
			k = re.sub("<|>|-|--", "", k)
			#print k,v
			setattr(self, k, v)
		return self
	
	def dispatch(self):
		'''Dispatching commands of Crawtext for actions or programming a task.
		(this part of the code non agnostic but the main item is project)'''
		#j = Job(self.project)
		if self.crawl is True:
			if self.find():
				#print "Restarting project %s" %self.project
				j = Job(self.project)
				if j.upsert():
					print "Crawl job for the project \"%s\" has been sucessful updated!" %self.project
				return
			else:
				if j.create():
					print "Crawl job for the project \"%s\" has been succesfully created!" %self.project
				return
		elif self.remove is True:
			if j.delete():
				print "Crawl job for the project \"%s\" has been succesfully deleted!" %self.project
			return
		
		else:
			#see other options
			print "Action for the project \"%s\" is not implemented yet. Aborting" %self.project
			return

	def find(self):
		if self.project in self.collection.distinct("project"):
			self.doc = self.collection.find_one({"project": self.project})
			self.id = self.doc["_id"]
			return True		
		else:
			return False

	def find_all(self):
		return [Job(n["project"]) for n in self.collection.find()]
	
	# def find(self, project_name = None):
	# 	if project_name is not None:
	# 		self.project = project_name
	# 	return self.collection.find_one({"project": self.project})
	# 	return Job(n["project"])

	def manage_all(self):
		'''running every JOB based on last_update'''
		today = date.today()
		for n in self.collection.find():
			self.project = n["project"]
			job = Job(self.project)
			print job.last_date
			job.run()
			job.update()
		return True

	# def manage_all(self):
	#see copy_reg pickle
	#https://docs.python.org/2/library/copy_reg.html
	# 	p = Pool(5)
	# 	p.map(self.manage, [n for n in self.collection.find()])
	
	def manage_job(self):
		'''running one project'''
		Job()
		job = self.find()
		job.run()
		job.update()
		return 

	
class Job():
	def __init__(self, project_name=None):
		'''Initializing projet with parameters stored in the manager database'''
		#Load the Taskmanager database
		if project_name is not None:
			self.name = project_name
		self.task_db = Database(TASK_MANAGER_NAME)
		self.collection = self.task_db.use_coll('tasks')
			
	def find(self, project_name=None):
		'''Finding an existing Job in Manager (Boolean)'''
		if project_name is not None:
			self.name = project_name
		if self.name in self.collection.distinct("project"):
			self.doc = self.collection.find_one({"project": self.name})
			print self.doc
			self.id = self.doc["_id"]
			return True		
		else:
			return False	
	
	def config(self):
		'''Getting params stored in manager db and store them into params attribute'''
		if self.name:
			params = self.collection.find_one({"project":self.name})
			self.map_params(params)
		else: 
			return False
	

	def map_params(self, params):
		'''Set Job params'''
		if params:
			for k, v in params.items():
				if k == "_id":
					k = "id"
				setattr(self, k, v)
			return self	
	
			
	def create(self, name= None):
		'''Creating a new Job into Manager'''
		#1.agnostic version 
		# self.data = {}
		# for k,v in self.__dic__:
		# 	if k not in ["db", "collection"]:
		# 		self.data[k] = v
		
		#self.collection.insert(data)
		#2.(non agnostic version)
		#defining scope of the crawler
		self.scope = "++"
		if self.sourcing is True :
			self.scope = '=='
		if self.query is not None:
			self.collection.insert({"project":self.project, 
										"query":[self.query], 
										"file":[self.file], 
										"key": [self.key],
										"scope": [self.scope],	
										"status": "created",
										"nb_crawl": 0,
										#rename firther to start date
										"crawl_date": [datetime.today()],
										"additional_data": data})

			self.doc = self.collection.find_one({"project": self.project})
			self.id = self.doc["_id"]
			return True
		else:
			print "No query specified, unable to create the crawl task!\n See help on how to configure your first project typing:\n python crawtext.py --help)"
			return False
			
	def upsert(self):
		'''Updating Job into Task Manager'''
		if self.query:	
			self.collection.update({"_id":self.id}, {"$push":{"query":self.query}}, True)
		if self.key:
			self.collection.update({"_id":self.id}, {"$push":{"key":self.key}}, True)
		if self.file:
			self.collection.update({"_id":self.id}, {"$push":{"filename":self.file}}, True)
		#en cas de changement de modèle ici méthode alternative pour ajouter:
		#chercher si elle existe et l'insérer
		self.update()
		return True
	
	def update(self):
		'''Activate the Job'''
		self.collection.update({"_id":self.id}, {"$push":{"date":datetime.today()}}, True)
		self.collection.update({"_id":self.id}, {"$inc":{"nb_crawl":1}}, True)
		self.collection.update({"_id":self.id}, {"$set":{"status":"Activate"}}, True)
		return True

	def deactivate(self):
		'''Deactivate the Job'''
		self.collection.update({"_id":self.id}, {"$set":{"status":"Deactivated"}}, True)
		return True
	
	def delete(self):
		'''Remove the Job'''
		if self.find():
			self.collection.remove({"project":self.project})
			return True
		else:
			print "No existing job \"%s\" found\n. Exiting..." %self.project
			return False
	
	def run(self):
		'''Run a crawler according to jobs parameters'''
		#Connect to existing project database
		# self.project_db = Database(self.name)
		# self.project_db.create_colls()
		crawler(self.name, self.query)


	# Existing results of Job in specific database
	def get_last_date(self, project_name=None):
		if self.name or project_name:
			self.last_date = self.date[-1]
			self.last_update = ((self.last_date).day, (self.last_date).month, (self.last_date).year, (self.last_date).hour, (self.last_date).minute)
			return self.last_update
	#Useless
	def get_sources(self):
		self.project_db = Database(self.name)
		self.project_db.create_colls()
		print self.project_db.sources.count(), "sources"
		self.sources = self.project_db.sources.find()
		print self.sources_items
		return self.sources_items

	def get_queue(self):
		self.project_db = Database(self.name)
		self.project_db.create_colls()
		print self.project_db.queue.count(), "waiting items"
		self.queue_items = self.project_db.queue.find()
		print self.queue_items
		return self.queue_items

	def get_log(self):
		self.project_db = Database(self.name)
		self.project_db.create_colls()
		print self.project_db.logs.count(), "logs"
		self.logs_items = self.project_db.logs.find()
		print self.logs_items	
		return self.logs_items

	def get_results(self):
		self.project_db = Database(self.name)
		self.project_db.create_colls()
		print self.project_db.results.count(), "results"
		self.logs_items = self.project_db.resuls.find()
		print self.results_items	
		return self.results_items	
	# def __repr__(self, project_name=None):
	# 	if self.name:
	# 		return str(self.collection.find_one({"project":self.name}))
	# 	elif project_name:
	# 		return str(self.collection.find_one({"project":project_name}))
	# 	else:
	# 		return str([n for n in self.collection.find()])
				
if __name__ == '__main__':
	j = Manager()
	j.manage_all()