#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database import Database
import datetime
import requests
import re

TASK_MANAGER_NAME = "manager"

class TaskManager():
	def __init__(self, docopt_args):
		'''Initializing projet with parameters stored in a projet database AND user input'''
		#Load the Taskmanager database
		self.task_db = Database(TASK_MANAGER_NAME)
		self.collection =self.task_db.create_coll('tasks')	
		#Load user input as attributes of TaskManager
		self.config(docopt_args)
		self.dispatch()

	def config(self, docopt_args):
		'''Mapping user parameters into object attributes'''
		for k, v in docopt_args.items():
			k = re.sub("<|>|-", "", k)
			#print k,v
			setattr(self, k, v)
		return self
	
	def dispatch(self):
		if self.crawl is True:
			if self.find():
				print "Restarting project %s" %self.project
				self.update()
				return
			else:
				print "No project \"%s\" found. Creating a new one" %self.project
				self.create()
				return
		elif self.remove is True:
			print "Deleting project %s" %self.project
			self.delete()
			return
		
		else:
			pass
			return 

	def find(self):
		'''Finding an existing project in the job db: Boolean'''
		if self.project in self.collection.distinct("project"):
			self.doc = self.collection.find_one({"project": self.project})
			self.id = self.doc["_id"]
			return True		
		else:
			return False	
			
	def create(self):
		'''Creating a new project into Task Manager'''
		print "Creating a project task"
		#1.agnostic version 
		# data = {}
		# for k,v in self.__dic__:
		# 	if k not in ["db", "collection"]:
			# data[k] = v
		# self.collection.insert(data)

		#2.(non agnostic version)
		try:
			self.collection.insert({"project":self.project, 
								"query":[self.query], 
								"file":[self.file], 
								"key": self.key, 
								"status": "created",
								"nb_crawl": 0,
								"crawl_date": [datetime.datetime.today()]})
			try:
				self.doc = self.collection.find_one({"project": self.project})
				self.id = doc["_id"]
				return self
			except Exception:
				return False
		except Exception:
			return False
		
	
	def update(self):
		'''Updating existing project into Task Manager'''
		print "updating project"
		if self.query:	
			self.collection.update({"_id":self.id}, {"$push":{"query":self.query}}, True)
		if self.key:
			self.collection.update({"_id":self.id}, {"$push":{"key":self.key}}, True)
		if self.file:
			self.collection.update({"_id":self.id}, {"$push":{"filename":self.file}}, True)
		self.activate()
		return self
	
	def activate(self):
		'''Activate the Task'''
		self.collection.update({"_id":self.id}, {"$push":{"date":datetime.datetime.today()}}, True)
		self.collection.update({"_id":self.id}, {"$inc":{"nb_crawl":1}}, True)
		self.collection.update({"_id":self.id}, {"$set":{"status":"Activate"}}, True)
		return self

	def deactivate(self):
		'''Deactivate the Task'''
		self.collection.update({"_id":self.id}, {"$set":{"status":"Deactivated"}}, True)
		return self
	
	def delete(self):
		'''Remove the Task'''
		if self.find():
			self.collection.remove({"project":self.project})
		else:
			print "No project \"%s\" found. Exiting"
		return
