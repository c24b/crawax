#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
manager.py
Utils to send CRON jobs with a mongodb collection 
that stores project and initial configuration given by user 
using crawtext script

"""
from datetime import datetime, date
from database import Database, TASK_MANAGER_NAME, TASK_COLL
from dispatcher import Dispatcher


class Manager():
	'''Simple task manager with info sent by user using crawtext '''
	def __init__(self, docopt_args=None):
		'''Initializing projet with parameters stored in a projet database AND user input'''
		#Load the Taskmanager database
		self.task_db = Database(TASK_MANAGER_NAME)
		self.collection =self.task_db.create_coll(TASK_COLL)	
		
		if docopt_args is None:
			'''run every jobs in task manager'''
			print "running every jobs in Manager"
			self.run()

		elif type(docopt_args) == str:
			'''manage an existing job'''
			print "running crawl for %s" %docopt_args
			self.run_job(docopt_args)

	def run(self):
		'''running every JOB present in TASK_MANAGER Database based on their status and their last date'''	
		for task in self.collection.find():
			print task["project"]
			self.task = task
			if self.is_active(): #and self.is_pending():
				Dispatcher(self.task)
		return 

	# def manage_all(self):
	def is_active(self):
		if self.task['status'] == "Active":
			return True
		else: return False

	def is_pending(self):
		today = datetime.today()
		if (self.task['date'][-1]).day != today.day:
			return True
		else: return False
	
	def activate_discover(self):
		'''Adding again search results or/and file to source and to queue'''
		if self.task["sourcing"] is True:
			return False
		if self.task["file"][-1] is not None or self.task["key"][-1] is not None:
			return True

	def run_job(self, task_name):
		'''running one project'''
		task = self.collection.find_one({"project": task_name})
		if self.is_active() and self.is_pending():
			return Dispatcher(self.task)


			

				
if __name__ == '__main__':
	j = Manager()
	