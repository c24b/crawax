from crawler import Crawler
from report import Report
from export import Export
from scheduler import Scheduler

class Dispatcher():
	'''Dispatcher for job in TASK_MANAGER database'''
	def __init__(self, job_params):
		self.task = job_params
		if self.task['crawl'] is True:
			c = Crawler(self.task)
			c.crawl()
		elif self.task['report'] is True:
		#crawtext.py report <project> [((--email=<email>| -e <email>) -u <user> -p <passwd>)| (-o <outfile> |--o=<outfile>)]
			Report(self.task)
		elif self.task['export'] is True:
		#crawtext.py export [results|sources|logs|queue]  <project> [(-o <outfile> |--o=<outfile>)] [-t <type> | --type=<type>]
			Export(self.task)	
		
		#Editing project
		elif self.task['stop'] is True:
			s = Scheduler(self.task)
			print s.deactivate()

		elif self.task['remove'] is True or self.task["delete"] is True:
			s = Scheduler(self.task)
			print s.delete()

		elif self.task['restart'] is True:
			s = Scheduler(self.task)
			print s.activate()
		# elif self.task['extract'] is True:
		#new method for extract every url
		else:
			raise NotImplemented
		
