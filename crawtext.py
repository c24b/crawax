#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Crawtext.
Description:
A simple crawler in command line.

Usage:
<<<<<<< HEAD
	crawtext.py crawl <name> <query> (-f <filename> | -k <key> | -f <filename> -k <key>) [--sourcing]
	crawtext.py report <name> [((--email=<email>| -e <email>) -u <user> -p <passwd>)| (-o <outfile> |--o=<outfile>)]
	crawtext.py export [results|sources|logs|queue]  <name> [(-o <outfile> |--o=<outfile>)] [-t <type> | --type=<type>]
	crawtext.py extract <name> <url>
	crawtext.py delete <name>
	crawtext.py run <name>
=======
	crawtext.py crawl <project> [<query>] [(-f <filename>|--file=<filename>) (-k <key> |--key=<key>)]
	crawtext.py remove <project> [...]
	crawtext.py restart <project> 
	crawtext.py stop <project> 
	crawtext.py report <project> [((--email=<email>| -e <email>) -u <user> -p <passwd>)| (-o <outfile> |--o=<outfile>)]
	crawtext.py export [results|sources|logs|queue]  <project> [(-o <outfile> |--o=<outfile>)] 
>>>>>>> 2159f47c7af2f1de4591e5291aefa74b6e09a939
	crawtext.py (-h | --help)
  	crawtext.py --version

Options:
<<<<<<< HEAD
	[crawl] schedule a crawl into Cortext Manager
	[report] schedule a report on current crawl sent by <mail> OR stored in <file> OR printed out
	[export] schedule a export the specified <collection> into a JSON file and then into a ZIP file
	[extract] schedule an extract of every page of a given <url>
	[delete] remove task
	[run] directly exceute the <task_name>
=======
	[crawl] launch a crawl
	[restart] restart the crawl
	[stop] stop the crawl
	[report] report on current crawl sent by <mail> OR stored in <file> OR printed out
	[export] export the specified <collection> into a JSON file and then into a ZIP file
>>>>>>> 2159f47c7af2f1de4591e5291aefa74b6e09a939
	-f --file Complete path of the sourcefile.
	-o --o Outfile format for export
	-k --key  Bing API Key for SearchNY.
	-e --email one or more emails separated by a coma
	-u gmail adress account to send report
	-p password of gmail account
	-h --help Show usage and Options.
	--version Show versions.  
'''

<<<<<<< HEAD
__all__ = ['crawtext', 'manager','database', "scheduler", "dispatcher"]

import __future__
from docopt import docopt
from scheduler import Scheduler
import sys
 
CRAWTEXT = "crawtext"
if __name__== "__main__":
		s = Scheduler()
		s.schedule(docopt(__doc__))
=======
__all__ = ['crawtext']

import __future__
import datetime

import sys
import subprocess
import re
from docopt import docopt
from database import Database
from page import Page
from crawtext_options import Discovery, Sourcing
from mongo_manager import TaskManager

from report import Report
from export import Export
from pymongo import errors as mongo_err

def crawler(docopt_args):
	start = datetime.datetime.now()
	db_name = docopt_args['<project>']
	query = docopt_args['<query>']
	
	db = Database(db_name)
	db.create_colls()
	while db.queue.count > 0:

		print "beginning crawl"
		print "Nombre de sources dans la base", db.sources.count()
		print "Nombre d'url à traiter", len(db.queue.distinct("url"))
		for url in db.queue.distinct("url"):
			if url not in db.results.find({"url":url}):
				p = Page(url, query)
				
				if p.check() and p.request() and p.control() and p.extract():
					#print "Links", p.outlinks
					db.results.update(p.info, {'$push': {"date": datetime.datetime.today()}}, upsert=True)
					#db.results.insert(p.info)
					if p.outlinks is not None:
						try:
							for n_url in p.outlinks:
								if n_url is not None or  n_url not in db.queue.find({"url":n_url}) or n_url not in db.results.find({"url":n_url}) or n_url not in db.log.find({"url":n_url}):
									# Checking correct url before is problematic
									# next_p = Page(n_url, query)
									# if next_p.clean_url(p.url) is not None:
									db.queue.insert({"url":n_url})
						except mongo_err:
							db.log.udpate({"url":url, "error_type": "pymongo error inserting outlinks", "query": self.query, "status":False},{'$push': {"date": datetime.datetime.today()}}, upsert=True)
				elif p.error_type != 0:
					''' if the page is not relevant do not store in db'''
					db.log.update(p.bad_status(),{"date": {'$push': datetime.datetime.today()}}, upsert=True)
				else:
					continue

			db.queue.remove({"url": url})
			if db.queue.count() == 0:
				print db.stats()
				break
			
		if db.queue.count() == 0:
			print db.stats()		
			break
		

	end = datetime.datetime.now()
	elapsed = end - start
	print "crawl finished, %i results and %i sources are stored in Mongo Database: %s in %s" %(db.results.count(),db.sources.count(),db_name, elapsed)
	return 

def crawtext(docopt_args):
	''' main crawtext run by command line option '''
	task = docopt_args['<project>']
	if docopt_args['crawl'] is True and docopt_args['<project>'] is not None:
		t = TaskManager(docopt_args)
		print t.doc
	elif docopt_args['remove'] is True and docopt_args['<project>'] is not None:
		t = TaskManager(docopt_args)
		t.remove()
		#print t.doc["date"][-1]
	# if docopt_args['discover'] is True:
	# 	print "Running discovery mode ..."
	# 	if docopt_args['<query>'] is not None:
	# 		Discovery(db_name=docopt_args['<project>'],query=docopt_args['<query>'], path=docopt_args['--file'], api_key=docopt_args['--key'])
	# 		Sourcing(db_name=docopt_args['<project>'])
	# 		crawler(docopt_args)
	# 		#s.db.queue.drop()
	# 		Export(docopt_args)
	# 		return "Discovery completed !"
	# 	else:
	# 		print "Discovery mode needs a query to search. Please check your arguments and try again"
	# 		print docopt_args['--help']
	# 		return False
	# 	#Scheduler using UNIX COMMAND
	# 	# if docopt_args['--repeat']:
	# 	# 	schedule(crawler, docopt_args)
	# 	# 	return sys.exit()
	
	# if docopt_args['crawl'] is True:
		
	# 	s = Sourcing(db_name=docopt_args['<project>'])
	# 	crawler(docopt_args)
	# 	print "sourcing completed.\nExporting"
	# 	Export(docopt_args)
	# 	print "Export completed.\nReport"
	# 	Report(docopt_args)
	# 	return True
	# 	#crawler(docopt_args)
	# 	# if docopt_args['--repeat']:
	# 		# schedule(crawler, docopt_args)
	# 		# return sys.exit()
	elif docopt_args['stop']:
		db = Database(docopt_args['<project>'])
		db.queue.drop()
		# unschedule(docopt_args)
		print ">>>Current queue is now empty. Process on project %s is stopped" %docopt_args['<project>']
		print db.stats()
		return False

	elif docopt_args['restart']:
		'''Option restart restarting the current queue without adding to sources'''
		db = Database(docopt_args['<project>'])
		
		if db.queue.count() <=0:
			print ">>>No data in current queue. Crawlin again with sourcefile"

			print "\nReloading initial config with sources data"
			s = Sourcing(db_name=docopt_args['<project>'])
			crawler(docopt_args)
			print db.stats()
			return
		else:
			print ">>>Restarting process on %s..." %(docopt_args['<project>'])
			crawler(docopt_args)
		#schedule(crawler, docopt_args)
		return 
	elif docopt_args['report']:
		print ">>>> Stats report on %s" %docopt_args['<project>']
		Report(docopt_args)
		return

	elif docopt_args['export']:
		Export(docopt_args)
		return
		
	else:
		print "No command supplied, please check command line usage and options."
		return sys.exit() 

if __name__ == "__main__":
	
	crawtext(docopt(__doc__))
	sys.exit()

>>>>>>> 2159f47c7af2f1de4591e5291aefa74b6e09a939
