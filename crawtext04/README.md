CRAWTEXT Simple CLI Crawler in Python
========================================================
==USING CRAWTEXT==

Here explanation of the crawtext
Simple command line interface to crawl the web
2 modes:
Crawl with an existing database
Discover new source and lauch crawler


==Instalation==

== PIP ==
You can install it using pip

    pip install crawtext
==Manual install ==
1. Install Mongo 
sudo apt-get install mongo-db mongo-client mongo-server
2. Install required libraries
pip install -r requirements.txt
setup_tools lxml (Problems with pip install version)
3. Install Goose extractor
git clone https://github.com/grangier/python-goose.git
cd python-goose
python setup.py install

==Usage Example==
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

    

This code is under XXX licence .