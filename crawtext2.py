#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Crawtext.
Description:
A simple crawler in command line.

Usage:
	crawtext archive [ -f (default|wiki|forum) ] <url>
	crawtext <user>
	crawtext <name>
	crawtext report <name>
	crawtext export <name>
	crawtext delete <name>
	crawtext <name> -u <email>
	crawtext <name> -q <query>
	crawtext <name> -s set <url>
	crawtext <name> -s append <file>
	crawtext <name> -k set <key>
	crawtext <name> -k append <key>
	crawtext <name> -s expand
	crawtext <name> -s delete [<url>]
	crawtext <name> -s delete					
	crawtext <name> -r (monthly|weekly|daily)
	
	crawtext (-h | --help)
  	crawtext --version
Options:
	Projets:
	# Pour consulter vos projets :	crawtext vous@cortext.net
	# Pour consulter un projet : 	crawtext pesticides
	# Pour obtenir un rapport : 	crawtext report pesticides
	# Pour obtenir un export : 		crawtext export pesticides
	# Pour supprimer un projet : 	crawtext delete pesticides
	Proprietaire:
	# pour définir le propriétaire du project: crawtext pesticides -u vous@cortext.net
	Requête:
	# pour définir la requête: crawtext pesticides -q "pesticides AND DDT"
	Sources:
	# pour définir les sources d'après un fichier :	crawtext pesticides -s set sources.txt	
	# pour ajouter des sources d'après un fichier :	crawtext pesticides -s append sources.txt
	# pour définir les sources d'après Bing :		crawtext pesticides -k set 12237675647
	# pour ajouter des sources d'après Bing :		crawtext pesticides -k append 12237675647
	# pour ajouter des sources automatiquement :	crawtext pesticides -s expand
	# pour supprimer une source :					crawtext pesticides -s delete www.latribune.fr
	# pour supprimer toutes les sources :			crawtext pesticides -s delete
	Récurrence
	# pour définir la récurrence :                	crawtext pesticides -r monthly|weekly|daily
'''

__all__ = ['crawtext', 'manager','database', "scheduler", "dispatcher"]

import __future__
from docopt import docopt
from scheduler import Scheduler
import sys


 
CRAWTEXT = "crawtext"
if __name__== "__main__":
		
	#~ user_input = docopt(__doc__)
		#~ is_valid = validate_email(user_input['<email>'])
		#~ if is_valid:
			#~ user_input['<name>'] = user_input['<email>']
		#~ else:
			
	s = Scheduler()
	s.schedule(docopt(__doc__))
