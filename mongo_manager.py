#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database import Database
import datetime
import requests
TASK_MANAGER_NAME = "manager"

class TaskManager():
	def __init__(self, docopt_args):
		'''Initializing projet with parameters stored in a projet database'''
		self.db = Database(TASK_MANAGER_NAME)
		self.collection =self.db.create_coll('tasks')

		self.map(docopt_args)		
		#self.config()
		self.doc = self.collection.find_one({"project":docopt_args['<project>']})
		self.run()

	def run(self, docopt_args):
		if (docopt_args['<filename>'] or docopt_args['<key>']) or docopt_args['<query>']:
				if doc is None:
					print "Creating a new task for project \"%s\"" %docopt_args['<project>']
					self.collection.insert(self.data)
					
				else:
					print "Task for \"%s\" project already exist" %docopt_args['<project>'] 
					print ">>>Updating configuration"
					self.update()
					#self.collection.update({"project": docopt_args['<project>']},{"$inc": {"data.nb_crawl": 1}}, True)
					
			elif docopt_args['<project>']:
				if doc is not None:
					print "Activating the task"
					self.activate()
					#self.update()
				else:
					print "No project \"%s\" found! \nPlease start your new project adding an API Key OR/AND a file path." %docopt_args['<project>']
					print "Type python crawtext.py --help to see basic instructions" 	 	
			
	def map(self, docopt_args):
		self.data = {	"project":docopt_args['<project>'],
						"query":[str(docopt_args['<query>']).decode("utf8")],
						"file":[str(docopt_args['<filename>']).decode("utf8")],
						"key": [str(docopt_args['<key>']).decode("utf8")],
						"date": [datetime.datetime.now()],
						"nb_crawl": 0,
						"status": "Created",
					
					}
		return self

	def create(self):
		'''Creating a new project into Task Manager'''
		print "Creating a New Task"
		#initial insert
		self.collection.insert({"project":self.project, "data":self.data})
		
		return self
	
	def update(self):
		'''Updating existing project into Task Manager'''
		self.doc = self.collection.find_one({"project": self.data["project"]})
		self.id = self.doc["_id"]			
		if self.data["query"] != self.doc["query"]:	
			self.collection.update({"_id":self.id}, {"$push":{"query":self.data["query"]}}, True)
		elif self.data["key"] != self.doc["query"]:
			print self.data["key"]
			self.collection.update({"_id":self.id}, {"$push":{"key":self.data["key"]}}, True)
		elif self.data["file"] != self.doc["file"]:
			print self.data["file"]
			self.collection.update({"_id":self.id}, {"$push":{"filename":self.data["file"]}}, True)
		else:
			pass
		self.activate()
		print "updated!"
		return self
	
	def activate(self):
		'''Activate the Task'''
		self.collection.update({"_id":self.id}, {"$push":{"date":datetime.datetime.now()}}, True)
		self.collection.update({"_id":self.id}, {"$inc":{"nb_crawl":1}}, True)
		self.collection.update({"_id":self.id}, {"$set":{"status":"Activated"}}, True)
		return

	def deactivate(self):
		'''Deactivate the Task'''
		self.collection.update({"_id":self.id}, {"$set":{"status":"Deactivated"}}, True)
		return
