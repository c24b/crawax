class Dispatcher():
	'''Dispatcher for job in TASK_MANAGER database'''
	def __init__(self, job_params):
		self.task = job_params
		if self.task['crawl'] is True:
			return Crawler(self.task)
		
		elif self.task['report'] is True:
		#crawtext.py report <project> [((--email=<email>| -e <email>) -u <user> -p <passwd>)| (-o <outfile> |--o=<outfile>)]
			return Report(self.task)
		elif self.task['export'] is True:
		#crawtext.py export [results|sources|logs|queue]  <project> [(-o <outfile> |--o=<outfile>)] [-t <type> | --type=<type>]
			return Export(self.task)	
		
		#Editing project
		elif self.task['stop'] is True:
			s = Scheduler(self.task)
			return s.deactivate()

		elif self.task['remove'] is True or self.task["delete"] is True:
			s = Scheduler(self.task)
			return s.delete()

		elif self.task['restart'] is True:
			s = Scheduler(self.task)
			return s.deactivate()
		# elif self.task['extract'] is True:
		#new method for extract every url
		else:
			raise NotImplemented
		
