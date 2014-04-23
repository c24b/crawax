CRAWTEXT Simple CLI Crawler in Python
========================================================
USING CRAWTEXT
----

Crawtext is a simple crawler in command line 
*discovery* stores the initial results of a search or/and sourcefile into a sources collections and then crawl with this existing sources collection (use it for the first run)
*crawl*  take the initial sources collections and crawl (use it if you want to monitor your initial database)


How does it work?
----

Crawtext take a search query and crawl the web using:
*	a sourcefile (.txt) 
(see sample file seeds.txt in repo)
* or/and a (BING SEARCH API KEY|http://datamarket.azure.com/dataset/bing/search)
Get an api key from BING  >> (http://datamarket.azure.com/dataset/bing/search)

For more informations about required options and how to use it refer to example or use
```bash
crawtext.py -h
```

It stores webpage that match a specific query into results collection.
The projectname correspond to the database name that store the results inside your Mongo db
This database contains 3 collections:
* 		sources 
* 		results 
*		logs (error info)
connect to mongo in shell to see the informations stored for each collection.
	   mongo <project_name>
	   > db.results.findOne() 

In case the process is stopped by the user, the queue treatment is saved for next run (and stored in a collection called queue in the database) you can restart process using command restart and clean the current queue using stop. 
Each initial source is stored in sources collection. 
Each error is stored in the database.

   
2 modes can be used:
  *	Discover : Create new entries in sources database and launch the crawler
  *	Crawl with an existing database: Base on an existing sources database (specified in the project_name), launch the crawler

New features:
----
*	report send an mail with actual stats of the database (put your own credentials into cfg.py and don't share it)
*	restart relaunch process if job was stopped
*	stop kill current process queue



Installation on Linux 
----
* Automatic install 
+install.sh 
```bash
chmod 750 install.sh
./install.sh
source bin/activate
```

install.sh create a virtualenv inside the project and download the libraries stored in requirements.txt 

Some extra featured are installed for this project asking for sudoers rights:
+[Virtualenv]
+[MongoDB] (https://www.mongodb.org/)
+``lxml`` using easy_install
+``libxml2`` ``libxml``
+ ``goose``[git|https://github.com/grangier/python-goose]
+ easylist.txt for Advertissement detection filter 



* Manual install

+ [MongoDB](https://www.mongodb.org/)
+ Dependencies
```
pip install -r requirements.txt
```
+ [goose](https://github.com/grangier/python-goose)
```bash
git clone https://github.com/grangier/python-goose.git
cd python-goose
sudo pip install -r requirements.txt
sudo python setup.py install
```

Installation on a mac
----

+ [MongoDB](https://www.mongodb.org/)

+ Dependencies

```sh
sudo pip install pymongo
sudo pip install docotp
sudo pip install tld
```

+ [goose](https://github.com/grangier/python-goose)

```bash
git clone https://github.com/grangier/python-goose.git
cd python-goose
sudo pip install -r requirements.txt
sudo python setup.py install
```

+ When running crawtext, python might fail import the *_imaging* module:

```
>>> import _imaging
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: dlopen(//anaconda/lib/python2.7/site-packages/PIL/_imaging.so, 2): Library not loaded: /opt/anaconda1anaconda2anaconda3/lib/libtiff.5.dylib
  Referenced from: //anaconda/lib/python2.7/site-packages/PIL/_imaging.so
  Reason: image not found
```

Reinstalling PIL might help:

```sh
sudo pip uninstall pil
pypath=`python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"` && cd $pypath && sudo rm -rf PIL
sudo pip install pil --allow-external pil --allow-unverified pil
```


Usage on Command Line
----

	Usage:
	crawtext.py <project> crawl <query> 
	crawtext.py <project> discover <query> [--file=<filename> | --key=<bing_api_key> | --file=<filename> --key=<bing_api_key>] [-v]
	crawtext.py <project> restart 
	crawtext.py <project> stop
	crawtext.py <project> report [--email=<email>]
	crawtext.py (-h | --help)
  	crawtext.py --version

Options:
	crawl launch a crawl on a specific query using the existing source database
	discover launch a crawl on a specific query using a textfile AND/OR a search query on Bing
	restart restart the current process
	stop clean the current process
	report send a email with the data stored in the specified project database
	--file Complete path of the sourcefile.
	--key  Bing API Key for SearchNY.
	--mail one or more emails separated by a coma
	-h --help Show usage and Options.
	--version Show versions.  

Example
---

With the Bing API key "1234567890", let's get 50 urls from bing and crawl them for the query "Algues Vertes":

```sh
python crawtext.py alguesVertes discover "Algues Vertes" --key=1234567890
```


