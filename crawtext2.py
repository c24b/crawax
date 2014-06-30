#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Crawtext.
Description:
A simple crawler in command line.

Usage:
	crawtext.py archive [ -f (default|wiki|forum) ] <url>
	crawtext.py <name>
	crawtext.py <email>
	crawtext.py report <name>
	crawtext.py export <name>
	crawtext.py delete <name>
	crawtext.py <name> -u <email>
	crawtext.py <name> -q <query>
	crawtext.py <name> -s set <url>
	crawtext.py <name> -s append <file>
	crawtext.py <name> -k set <key>
	crawtext.py <name> -k append <key>
	crawtext.py <name> -s expand
	crawtext.py <name> -s delete [<url>]
	crawtext.py <name> -s delete					
	crawtext.py <name> -r (monthly|weekly|daily)
	
	crawtext.py (-h | --help)
  	crawtext.py --version
Options:
	Projets:
	# Pour consulter un projet : 	crawtext pesticides
	# Pour consulter vos projets :	crawtext show vous@cortext.net
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
from scheduler2 import Scheduler
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
	
