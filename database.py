#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
from pymongo import MongoClient
from pymongo import errors

class Database(object):
	'''Database creation''' 
	def __init__(self, database_name):
		self.name = database_name
		client = MongoClient('mongodb://localhost,localhost:27017')
		self.db = client[self.name]
		#self.db.x = self.db[x]
		
	def __repr__(self, database_name):	
		return self.name
		
	def create_tables(self):
		self.results = self.db['results']
		self.queue = self.db['queue'] 
		self.log = self.db['log']
		self.sources = self.db['sources']
		return self
	
	def create_table(self, name):
		self.name= self.db[name]
		return self.db[name]
