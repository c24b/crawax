CRAWTEXT Simple CLI Crawler in Python
========================================================
USING CRAWTEXT
----

Crawtext is a simple crawler in command line. For each project it creates
a mongodatabase with 3 collections
sources info, results and logs info (error)

2 modes can be used:
  *	Crawl with an existing database
  *	Discover new source and lauch crawler
Just activate -h for information about how to use it

Installation
---
Please make sure that you have **mongodb** installed

Make install.sh executable (chmod 750 install.sh)
install create a virtualenv inside the project and download the libraries stored in requirements.txt

To use crawtext please first enter in command line:
source bin/activate
	
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

    
This code is under ??? licence .
