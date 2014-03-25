#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apscheduler.scheduler import Scheduler
from apscheduler.jobstores.mongodb_store import MongoDBJobStore
import time  
from pymongo import MongoClient
def schedule(docopt_args, job):
	if docopt_args['--repeat'] or docopt_args['start']:
		#mongo = pymongo.Connection(host='127.0.0.1', port=27017) 
		client = MongoClient('mongodb://localhost,localhost:27017')
		collection = client.jobs
		store = MongoDBJobStore(connection=collection)  
		sched = Scheduler(daemonic = False)
		sched.add_jobstore(store, 'mongo')
		sched.add_cron_job(job, day_of_week='mon', hour=5, minute=30, jobstore=store)
		shed.start()
		print "Job %s is actually running every Monday @5:30" %docopt_args['<project>'] 
		return

def unschedule(docopt_args):
	client = MongoClient('mongodb://localhost,localhost:27017')
	collection = client.jobs
	store = MongoDBJobStore(connection=collection)  
	sched = Scheduler(daemonic = False)
	#sched.shutdown(wait=True, shutdown_threadpool=True, close_jobstores=True)
	try:
		sched.unschedule_job(store)
		print sched.get_jobs()
	except KeyError:
		print "No job called %s is actually scheduled" %docopt_args['<project>']
		if sched.get_jobs() != []:
			print "Actual jobs scheduled:"
			for n in sched.get_jobs():
				print "-",n
	return