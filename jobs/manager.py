	#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import requests
import re

from database import Database

TASK_MANAGER_NAME = "manager"

class Manager():
	'''Simple task manager with a Mongo db modules Database for CRUD operations'''
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
			k = re.sub("<|>|-|--", "", k)
			#print k,v
			setattr(self, k, v)
		return self
	
	def dispatch(self):
		'''Dispatching commands of Crawtext for actions or programming a task.
		(this part of the code non agnostic but the main item is project)'''
		if self.crawl is True:
			if self.find():
				#print "Restarting project %s" %self.project
				if self.update():
					print "Crawl job for the project \"%s\" has been sucessful updated!" %self.project
				return
			else:
				if self.create():
					print "Crawl job for the project \"%s\" has been succesfully created!" %self.project
				return
		elif self.remove is True:
			if self.delete():
				print "Crawl job for the project \"%s\" has been succesfully deleted!" %self.project
			return
		
		else:
			#see other options
			print "Action for the project \"%s\" is not implemented yet. Aborting" %self.project
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
		#1.agnostic version 
		# data = {}
		# for k,v in self.__dic__:
		# 	if k not in ["db", "collection"]:
			# data[k] = v
		# self.collection.insert(data)

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
										"crawl_date": [datetime.datetime.today()]})

			self.doc = self.collection.find_one({"project": self.project})
			self.id = self.doc["_id"]
			return True
		else:
			print "No query specified, unable to create the crawl task!\n See help on how to configure your first project typing:\n python crawtext.py --help)"
			return False
		
	
	def update(self):
		'''Updating existing project into Task Manager'''
		if self.query:	
			self.collection.update({"_id":self.id}, {"$push":{"query":self.query}}, True)
		if self.key:
			self.collection.update({"_id":self.id}, {"$push":{"key":self.key}}, True)
		if self.file:
			self.collection.update({"_id":self.id}, {"$push":{"filename":self.file}}, True)
		#en cas de changement de modèle ici méthode alternative pour ajouter:
		#chercher si elle existe et l'insérer
		self.activate()
		return True
	
	def activate(self):
		'''Activate the Task'''
		self.collection.update({"_id":self.id}, {"$push":{"date":datetime.datetime.today()}}, True)
		self.collection.update({"_id":self.id}, {"$inc":{"nb_crawl":1}}, True)
		self.collection.update({"_id":self.id}, {"$set":{"status":"Activate"}}, True)
		return True

	def deactivate(self):
		'''Deactivate the Task'''
		self.collection.update({"_id":self.id}, {"$set":{"status":"Deactivated"}}, True)
		return True
	
	def delete(self):
		'''Remove the Task'''
		if self.find():
			self.collection.remove({"project":self.project})
			return True
		else:
			print "No project \"%s\" found. Exiting" %self.project
			return False
