#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Crawtext.
Description:
A simple crawler in command line.

Usage:
	crawtext.py crawl <project> <query> [(-f <filename>|--file=<filename>) (-k <key> |--key=<key>)] [--sourcing]
	crawtext.py (remove|delete) <project> 
	crawtext.py restart <project> 
	crawtext.py stop <project> 
	crawtext.py report <project> [((--email=<email>| -e <email>) -u <user> -p <passwd>)| (-o <outfile> |--o=<outfile>)]
	crawtext.py export [results|sources|logs|queue]  <project> [(-o <outfile> |--o=<outfile>)] [-t <type> | --type=<type>]
	crawtext.py run [project]
	crawtext.py (-h | --help)
  	crawtext.py --version

Options:
	[crawl] launch a crawl
	[restart] restart the crawl
	[stop] stop the crawl
	[report] report on current crawl sent by <mail> OR stored in <file> OR printed out
	[export] export the specified <collection> into a JSON file and then into a ZIP file
	-f --file Complete path of the sourcefile.
	-o --o Outfile format for export
	-k --key  Bing API Key for SearchNY.
	-e --email one or more emails separated by a coma
	-u gmail adress account to send report
	-p password of gmail account
	-h --help Show usage and Options.
	--version Show versions.  
'''

__all__ = ['crawtext', 'manager','database', "scheduler", "dispatcher"]

import __future__
from docopt import docopt
from scheduler import Scheduler
import sys
 
CRAWTEXT = "crawtext"
if __name__ == "__main__":
	'''sending job to be done'''
	s = Scheduler(docopt(__doc__))
	s.schedule()
	sys.exit()


