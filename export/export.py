#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, datetime
import subprocess
from string import upper

class Export():
	'''special method to export projet collections'''
	def __init__(self, docopt_args):
		start = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
		argv = ['mongoexport', '-d', docopt_args['<project>'], '-c', 'results', '--jsonArray', '-o', 'report.json']
		if docopt_args['--o']:
			argv[7] = docopt_args['--o']
		else:
			argv[7] = "EXPORT_"+docopt_args['<project>']+"_"+start+"_.json"
		
		if docopt_args['sources']:	
			argv[4] = "sources"
			
		elif docopt_args['logs']:	
			argv[4] = "log"
			
		elif docopt_args['queue']:
			argv[4] = "queue"
			
		else:
			#defaut is results export
			argv[4] = "results"
		
		argv[7] = upper(argv[4])+"_"+docopt_args['<project>']+"_"+start+"_.json"
		outfile = re.split("\.", argv[7])[0]
		subprocess.call(argv)
		subprocess.call(['zip', outfile+".zip", argv[7]])
		