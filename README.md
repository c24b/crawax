CRAWTEXT Simple CLI Crawler in Python
========================================================
USING CRAWTEXT
----

Crawtext is a simple crawler in command line it take a search query and crawl the web using a sourcefile (.txt) or/and a API key for BING (see here to get your BING API KEY). It stores webpage that match a specific query into results collection.
The projectname correspond to the database name that store the results
This database contains 3 collections:
* 		sources 
* 		results 
*		logs (error info)
connect to mongo in shell to see the informations stored for each collection.
	   mongo <project_name>
	   > db.results.findOne() 

In case the process is stopped by the user, the queue treatment is saved for next run (and stored in a collection called queue in the database). each initial source is stored in sources collection. Each error is stored in the database.

   
2 modes can be used:
  *	Discover : Create new entries in sources database and launch the crawler
  *	Crawl with an existing database: Base on an existing sources database (specified in the project_name), launch the crawler

Just activate -h for information about options required and how to use it

Installation
---
Please make sure that you have **mongodb** installed

Make install.sh executable (chmod 750 install.sh)
install.sh create a virtualenv inside the project and download the libraries stored in requirements.txt (some extra featured are installed for this project such as Goose not availale throught pip) and lxml via easy_install

To use crawtext please first enter in command line:
source bin/activate inside the current directory
	
Usage on Command Line
----
	Usage:
		crawtext.py <project> crawl <query> [--repeat]
     	 	crawtext.py <project> discover <query> [--file=<filename> | --key=<bing_api_key> | --file=<filename> --key=<bing_api_key>] [--repeat]
      	 	crawtext.py <project> start <query>
      	 	crawtext.py <project> stop
      	 	crawtext.py (-h | --help)
      	 	crawtext.py --version

	Options:
			--file Complete path of the sourcefile.
			--key  Bing API Key for Search.
			--repeat Scheduled task for every monday @ 5:30.
			-h --help Show usage and Options.
			--version Show versions.

    
This code is under GPL2 licence (as far as I know).

