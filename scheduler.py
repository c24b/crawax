#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
manager.py
Utils to send CRON jobs with a mongodb collection 
that stores project and initial configuration given by user 
using crawtext script

"""
from datetime import datetime
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
			#iteration over a certain type of info
			if k in ["query","file","key", "date"]:
				setattr(self.job, k, [v])
			else:
				setattr(self.job, k, v)
	
	def schedule(self):
		if self.find_task() is False:
			print self.create()
			return

	def find_task(self):
		'''Finding an existing project and comparing last arguments with new ones'''
		
		task = self.collection.find_one({"project":self.job.name})
		if task is not None:
			print "An existing project called \"%s\" has been found" %self.job.project
			self.upgrade(task)
			print self.update()
			return True
		else:
			return False

	def create(self):
		self.collection.insert(self.job.__dict__)
		return "Project %s has been succesfully created!" %self.job.project
	
	def upgrade(self, task):
		print "Checking for changes in parameters..."
		for k, v in task.items():
			try:
				value = v[0]
			except TypeError:
				value = v
			if value is not None or value != "":
				try:
					if task[k] != self.job.__dict__[k]:
						if k in ["date", "nb_crawl", "status"]:
							#it will be updated after
							pass
						elif type(self.job.__dict__[k]) != list:					
							self.collection.update({"project":self.job.project}, {"$set":{k:value}}, True)
							print "Project %s upgraded with a different %s info" %(self.job.project, k)
						else:
							if task[k] != self.job.__dict__[k][0]:	
								self.collection.update({"project":self.job.project}, {"$push":{k:value}}, True)
								print "Project %s upgraded with a different %s info" %(self.job.project, k)
						self.job.__dict__[k] = task[k]
				except KeyError:
					#Key error append because of _id that we don't want to upgrade!
					pass
		return 
	def update(self):
		self.collection.update({"project":self.job.project}, {"$push":{"date":datetime.today()}}, True)
		self.collection.update({"project":self.job.project}, {"$inc":{"nb_crawl":1}}, True)
		self.collection.update({"project":self.job.project}, {"$set":{"status":"Active"}}, True)		
		return "Project %s has been successfully updated!" %self.job.project
	
	def activate(self):
		self.collection.update({"project":self.job['project']}, {"$set":{"status":"Active"}}, True)
		return "Project %s has been sucessfully activated!" %self.job.project
	
	def deactivate(self):
		self.collection.update({"project":self.job['project']}, {"$set":{"status":"Inactive"}}, True)
		return "Project %s has been sucessfully deactivated!" %self.job.project
	
	def delete(self):
		self.collection.remove({"project":self.job['project']})
		return "Project %s has been sucessfully deleted" %self.job.project


