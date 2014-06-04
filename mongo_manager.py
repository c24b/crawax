#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database import Database
import datetime
import requests

TASK_MANAGER_NAME = "manager"

class TaskManager():
	def __init__(self, docopt_args):
		'''Initializing projet with parameters stored in a projet database'''
		self.task_db = Database(TASK_MANAGER_NAME)
		self.collection =self.task_db.create_coll('tasks')
		self.doc = self.collection.find_one({"project":docopt_args['<project>']})
		self.map(docopt_args)		
		#self.config()
		
		self.run()

	def run(self):
		if self.doc['<project>']:
			if self.doc is None:
				if docopt_args['<filename>']:
					self.map(docopt_args)
					print "Creating a new task for project \"%s\"" %docopt_args['<project>']
					self.collection.insert(self.data)
					return self
				elif docopt_args['<key>']:
					self.map(docopt_args)
					print "Creating a new task for project \"%s\"" %docopt_args['<project>']
					self.collection.insert(self.data)
					return self
				else:
					print "No project configuration for \"%s\" has been found! \nPlease start your new project adding an API Key OR/AND a file path." %docopt_args['<project>']
					print "Type python crawtext.py --help to see basic instructions"
					return False
			else:
				print "Task for \"%s\" project already exist" %docopt_args['<project>'] 
				if docopt_args['<filename>']:			
					print "Adding new configuration for project :%s" %docopt_args['<project>'] 
					self.update()
					return self
				elif docopt_args['<key>']:
					print "Adding new configuration for project :%s" %docopt_args['<project>'] 
					self.update()
					return self
				else:
					if self.doc["key"] or self.doc["filename"]:
						print "Reactivate the task with last configuration"
						print self.doc
						self.activate()
						return self
					else:
						print "No project configuration for \"%s\" has been found! \nPlease start your new project adding an API Key OR/AND a file path." %docopt_args['<project>']
						print "Type python crawtext.py --help to see basic instructions"
						return False
	def map(self, docopt_args):
		'''mapping console param to data'''
		self.data = {	"project":docopt_args['<project>'],
						"query":[str(docopt_args['<query>']).decode("utf8")],
						"file":[str(docopt_args['<filename>']).decode("utf8")],
						"key": [str(docopt_args['<key>']).decode("utf8")],
						"date": [datetime.datetime.today()],
						"nb_crawl": 0,
						"status": "Created",
					
					}
		return self.data
	def find_project(self):
		self.map()
		print self.data["project"]
		self.collection.find({	"project":self.data["project"]})
		
	def create(self):
		'''Creating a new project into Task Manager'''
		print "Creating a New Task"
		#initial insert
		self.collection.insert({"project":self.project, "data":self.data})
		
		return self
	
	def update(self):
		'''Updating existing project into Task Manager'''
		self.map()
		self.id = self.doc["_id"]			
		if self.data["query"] != self.doc["query"]:	
			self.collection.update({"_id":self.id}, {"$push":{"query":self.data["query"]}}, True)
		elif self.data["key"] != self.doc["query"]:
			self.collection.update({"_id":self.id}, {"$push":{"key":self.data["key"]}}, True)
		elif self.data["file"] != self.doc["file"]:
			self.collection.update({"_id":self.id}, {"$push":{"filename":self.data["file"]}}, True)
		else:
			pass
		self.activate()
		return self
	
	def activate(self):
		'''Activate the Task'''
		self.id = self.doc["_id"]
		self.collection.update({"_id":self.id}, {"$push":{"date":datetime.datetime.today()}}, True)
		self.collection.update({"_id":self.id}, {"$inc":{"nb_crawl":1}}, True)
		self.collection.update({"_id":self.id}, {"$set":{"status":"Activate"}}, True)
		return self

	def deactivate(self):
		'''Deactivate the Task'''
		self.collection.update({"_id":self.id}, {"$set":{"status":"Deactivated"}}, True)
		return self
	def remove(self):
		'''Remove the Task'''
		self.map()
		self.project = self.doc["project"]
		self.doc = self.collection.find({"project":self.project})
		for n in self.doc:
			print n
			# self.collection.remove({"project":self.project})
		return self

class Dispatch():
	def __init__(self):
		self.task_db = Database(TASK_MANAGER_NAME)
		self.collection =self.task_db.create_coll('tasks')
		self.doc = self.collection.find_one({"project":docopt_args['<project>']})
