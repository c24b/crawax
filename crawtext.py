#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Crawtext.
Description:
A simple crawler in command line.

Usage:
	crawtext.py crawl <name> <query> (-f <filename> | -k <key> | -f <filename> -k <key>) [--sourcing]
	crawtext.py report <name> [((--email=<email>| -e <email>) -u <user> -p <passwd>)| (-o <outfile> |--o=<outfile>)]
	crawtext.py export [results|sources|logs|queue]  <name> [(-o <outfile> |--o=<outfile>)] [-t <type> | --type=<type>]
	crawtext.py extract <name> <url>
	crawtext.py delete <name>
	crawtext.py run <name>
	crawtext.py (-h | --help)
  	crawtext.py --version

Options:
	[crawl] schedule a crawl into Cortext Manager
	[report] schedule a report on current crawl sent by <mail> OR stored in <file> OR printed out
	[export] schedule a export the specified <collection> into a JSON file and then into a ZIP file
	[extract] schedule an extract of every page of a given <url>
	[delete] remove task
	[run] directly exceute the <task_name>
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
if __name__== "__main__":
		s = Scheduler()
		s.schedule(docopt(__doc__))
