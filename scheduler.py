#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apscheduler.scheduler import Scheduler
from apscheduler.jobstores.mongodb_store import MongoDBJobStore
from apscheduler.scheduler import SchedulerEvent, JobStoreEvent
#from apscheduler.jobstores.mongodb import MongoDBJobStore
import time, sys  
import pymongo
import atexit
from database import Database

def schedule(function, docopt_args):
	if docopt_args['--repeat'] or docopt_args['start']:
		client = MongoClient('mongodb://localhost,localhost:27017')
		db = client[docopt_args['<project>']
		jobs.
		
		# mongo = pymongo.Connection(host='127.0.0.1', port=27017)
		# db = Database(docopt_args['<project>'])
		jobs = db['jobs']
		store = MongoDBJobStore(database=db, collection=jobs, connection=mongo)
		#store = MongoDBJobStore(connection=mongo, collection=collection)  
		sched = Scheduler(daemonic = False)
		#sched.add_jobstore(store, docopt_args['<project>'])
		print sched.get_jobs()
		#adding a job type cron as in docs  
		#sched.add_job(job, 'cron', {'year': 2014, 'day_of_week': 'mon-fri', 'hour': 5, 'minute': 30, 'second':0})
		sched.start()
		sched.add_cron_job(function, name=docopt_args['<project>'], day_of_week='mon-fri', hour=5, minute=30,args=docopt_args, misfire_grace_time=5, jobstore=store)
		print sched.get_jobs()
		print "Job %s is actually running every Monday @5:30" %docopt_args['<project>'] 
		atexit.register(lambda: sched.shutdown(wait=False))
		return shed

def unschedule(docopt_args):
	#mongo = pymongo.Connection(host='127.0.0.1', port=27017)
	db = Database()
	#collection = mongo.jobs
	#store = MongoDBJobStore(connection=collection)  
	sched = Scheduler(daemonic = False)
	#sched.shutdown(wait=True, shutdown_threadpool=True, close_jobstores=True)
	try:
		print sched.get_jobs()
		sched.unschedule_job(name=docopt_args['<project>'])
	except KeyError:
		print "No job called %s is actually scheduled" %docopt_args['<project>']
		if sched.get_jobs() != []:
			print "Actual jobs scheduled:"
			for n in sched.get_jobs():
				print "-",n
	return shed