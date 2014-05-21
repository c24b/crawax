#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from database import Database
class Export():
	'''special method to export projet collections'''
	def __init__(self, docopts_args):
		#print docopts_args
		self.db = Database(docopts_args['<project>'])
		self.db.create_tables()
		self.format = re.split("\.", docopts_args['--o'])[1]
		self.results = []
		print self.format
		self.filename = docopts_args['--o']
		self.db.create_tables()
		if docopts_args['results']:
			self.results.append([n for n in self.db.results.find()])
			
		elif docopts_args['sources']:
			self.results.append([n for n in self.db.sources.find()])
			
		elif docopts_args['logs']:
			self.results.append([n for n in self.db.logs.find()])
			
		elif docopts_args['queue']:
			self.results.append([n  for n in self.db.queue.find()])
			
		else:
			pass
		self.results = {"results":self.results}
		with open(self.filename, "wb") as fd:
			fd.write(str(self.results).encode("utf-8"))
