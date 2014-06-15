#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
manager.py
Utils to send CRON jobs with a mongodb collection 
that stores project and initial configuration given by user 
using crawtext script

"""
from datetime import datetime, date
from database import Database
from job import Job
import re
MANAGER = "Manager"
Tasks = "Jobs"
TASK_MANAGER_NAME = "manager"

class Scheduler(object):
	'''Scheduler send job to Task manager'''
	def __init__(self, params):
		self.task_db = Database(TASK_MANAGER_NAME)
		self.collection =self.task_db.create_coll('tasks')
		
		self.job = Job(params['<project>'])
		for k, v in params.items():
			k = re.sub("<|>|-|--", "", k)
			setattr(self.job, k, v)
		
	def find_task(self):
		'''Finding an existing project and comparing last arguments with new ones'''
		
		task = self.collection.find_one({"project":self.job.name})
		if task is not None:
			print "A project %s has been found" %self.job.project
			for k, v in tasks.items():
				if task[k] != self.job[k]:
					print "updating value"
					self.collection.update({"project":self.job.project}, {"$push":{k:v}}, True)
					self.job[k] = task[k]
			self.udpate()
			return True
		else:
			self.create()
			return False

	def create(self):
		
		self.job.start_date = date.today()
		self.job.nb_crawl = 0
		self.job.query = [self.job.query]
		self.job.file = [self.job.file]
		self.job.key = [self.job.key]
		self.job.date = [date.today()]
		for k, v in self.job.items():
			print k, v
		self.collection.insert(self.job)
		return "Project %s has been create" %self.job["project"]
	
	def update(self):
		self.collection.update({"project":self.job['project']}, {"$push":{"date":datetime.today()}}, True)
		self.collection.update({"project":self.job['project']}, {"$inc":{"nb_crawl":1}}, True)
		self.collection.update({"project":self.job['project']}, {"$set":{"status":"Active"}}, True)		
		return "Project %s has been updated" %self.job['project']
	
	def deactivate(self):
		self.collection.update({"project":self.job['project']}, {"$set":{"status":"Inactive"}}, True)
		return "Project %s has been deactivated" %self.job['project']
	
	def delete(self):
		self.collection.remove({"project":self.job['project']})
		return "Project %s has been deactivated" %self.job['project']


