################################
### Archiver un site complet ###
################################

python crawtext.py archive [ -f default|wiki|forum ] www.lemonde.fr

#########################
### Définir un projet ###
#########################

python crawtext.py
	# Pour consulter vos projets : python crawtext.py vous@cortext.net

python crawtext.py constance@cortext.net
	pesticides
	brevet
	# Pour consulter un projet  : python crawtext.py pesticides
	# Pour obtenir un rapport   : python crawtext.py report pesticides
	# Pour obtenir un export    : python crawtext.py export pesticides
	# Pour supprimer un projet  : python crawtext.py delete pesticides

python crawtext.py pesticides
	Propriétaire
		constance@cortext.net
	Requête
		"pesticides AND DDT"
		# pour définir la requête                    : python crawtext.py pesticides -q "pesticides AND DDT"
	Sources (4)
		www.lemonde.fr
		www.nouvelobs.fr
		www.latribune.fr
		www.lesechos.fr
		# pour définir les sources d'après un fichier : python crawtext.py pesticides -s set sources.txt
		# pour définir les sources d'après Bing       : python crawtext.py pesticides -s set 12237675647
		# pour ajouter des sources d'après un fichier : python crawtext.py pesticides -s append sources.txt
		# pour ajouter des sources d'après Bing       : python crawtext.py pesticides -s append 12237675647
		# pour ajouter des sources automatiquement    : python crawtext.py pesticides -s expand
		# pour supprimer une source                   : python crawtext.py pesticides -s delete www.latribune.fr
		# pour supprimer toutes les sources           : python crawtext.py pesticides -s delete
	Récurrence
		mensuel
		# pour définir la récurrence                 : python crawtext.py pesticides -r monthly|weekly|daily

#######################
### Base de données ###
#######################
Base:Crawtext
	Collection:Tasks
	Collection:Queue
	Collection:Logs
	Collection:Pages


start = element task {
	type: { archive|explore },
	( element archive {
		element domain { xsd:string },
		element format { default|wiki|forum }
	} | element explore {
		element owner       { xsd:email },
		element projectName { xsd:string },
		element cron        { none|monthly|weekly|daily },
		element query       { xsd:string },
		element sources     {
			element url { xsd:url },
			element created_at { xsd:dateTime },
			element origin { user|bing|expand },
		}+
	} ),
	element created_at  { xsd:dateTime }
}
