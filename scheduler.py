#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apscheduler.scheduler import Scheduler
from apscheduler.jobstores.mongodb_store import MongoDBJobStore
import time  

def schedule(docopt_args):
	if docopt_args['--repeat']:
		mongo = pymongo.Connection(host='127.0.0.1', port=27017)  
		store = MongoDBJobStore(connection=docopt_args['<project>'])  
		sched = Scheduler(daemonic = False)
		sched.add_jobstore(store, 'mongo')
		n = Crawler(db_name=docopt_args['<project>'], query=docopt_args)
		sched.add_cron_job(n.crawl(), day_of_week='mon', hour=5, minute=30, jobstore=docopt_args['<project>'])
		shed.start()
		print sched.print_jobs()
		return True
def unschedule(docopt_args):
	sched = Scheduler(daemonic = False)
	return sched.remove_jobstore(docopt_args['<project>'], close=True)
	