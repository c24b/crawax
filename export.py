#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from database import Database
class Export():
	'''special method to export projet collections'''
	def __init__(self, docopts_args):
		print docopts_args
		self.db = Database(docopts_args['<project>'])
		self.db.create_tables()
		self.format = re.split("/.", docopts_args['--o'])
		self.filename = docopts_args['--o']
		for i in self.db.__dict__:
			print i
		for n in self.db.results.find():
			print n

