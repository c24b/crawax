from crawler import Crawler
from report import Report
from export import Export
from scheduler import *

class Dispatcher():
	'''Dispatcher for job in TASK_MANAGER database'''
	def __init__(self, job_params):
		self.task = job_params
		try:
			if self.task['crawl'] is True:
				c = Crawler(self.task)
				c.crawl()
			elif self.task['report'] is True:
			#crawtext.py report <project> [((--email=<email>| -e <email>) -u <user> -p <passwd>)| (-o <outfile> |--o=<outfile>)]
				Report(self.task)
			elif self.task['export'] is True:
			#crawtext.py export [results|sources|logs|queue]  <project> [(-o <outfile> |--o=<outfile>)] [-t <type> | --type=<type>]
				Export(self.task)	
					
			# elif self.task['extract'] is True:
			#new method for extract every url
			
		except KeyError:
			print self.task["project"]
			print "Project %s not configured properly" %str(self.task["project"])
			
			s = Scheduler(self.task)
			s.delete()
			print "deleting project"
