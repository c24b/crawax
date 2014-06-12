#!/usr/bin/env python
# -*- coding: utf-8 -
from manager import Manager
from database import Database
from crawler import crawler
from datetime import date
TASK_MANAGER_NAME = "manager"

class Jobs():
	def __init__(self):
		'''Initializing projet with parameters stored in a projet database'''
		#Load the Taskmanager database
		self.task_db = Database(TASK_MANAGER_NAME)
		self.collection = self.task_db.use_coll('tasks')
		#self.collection = self.task_db['tasks']
	
	def run(self):
		if len(self.collection.distinct("_id")) > 0:
			for n in self.collection.find():
				#mapping the configuration found in tasks db 
				print "Running", n["project"], "..."
		 		try: 
		 			nodissc = n["scope"]

		 			Sourcing(n)
		 		except KeyError:
		 			Discovery(n)
		 			Sourcing(n)

		 		crawler(n)
		 		# Sourcing(n)
		 		# crawler(n)
		 		
			return
		else:
			print "No current tasks awaiting"
		return
	
	def run_job(self, project_name):
		docopt_args = self.collection.find_one({"project":project_name})
		#self.get_params(docopt_args)
		t = Manager(docopt_args)
		t.find()
		t.update()
		crawler(docopt_args)

	
	def __repr__(self):
		for n in self.collection.find():
			print "======"
			print "parameters for %s" %n["project"]
			for k, v in n.items():
				print k,"=\t", v
			print "\n"  
		return 

	def cron(self):
		now = date.today()
		for n in self.collection.find():
			last = n["date"][-1]
			print last.year,last.month, last.day
			print now.day - last.day
			if now.day - last.day >= 0:
				print "To be updated"
				self.run_job(n["project"])
				
				
