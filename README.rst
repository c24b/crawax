Description
=======
This program allows one to automatically get search content on the web,
starting from words to search ("bee", "dans le cochon tout est bon", "Green Alga OR escheria", "procrastination AND useful") 
and following the links for each page that contains this specific word or expression. 
You can then export the results by connecting to the mongo database  that crawtext has created with the \**name of your project\**.
 
Dependencies
============
- MongoDB <https://www.mongodb.org/>
- python-lxml 
- ``python-goose`` <https://github.com/grangier/python-goose.git>
- ``pymongo``
- ``docopt``
- ``python-requests``

See requirements.txt for the complete list of dependencies

INSTALLATION
=======
The first two steps are designed for a Debian based distribution as they involve installing packages (MongoDB and LXML) with apt-get. 

Automatic install on Debian
--------------------
A bash file is provided to install all dependencies on Debian Based distribution  run``./install.sh`` will create a virtual environnemet to setup crawtext dependencies

Multiples repository for Mongodb are available for Debian based distribution and not compatible. Choose carefully the way to install MongoDB from debian packages sources or 10gen packages. The different versions  might not be compatible. 
See in the "Read More" section the links to the install pages of these softwares.

MongoDB requires to have an existing /data/db directory .

 | Note: to install mongo a defaut directory is required by mongo so you have to create it ``sudo mkdir /data/db``

 
Manual install on Debian
------------------

You can install all the dependencies crawtext relies upon. 
It is recommended to install ``virtualenv`` to set up a virtual environment in order not to disturb other programs. 

Install the packages
::
    sudo apt-get install python-dev mongodb-10gen python-lxml 
    sudo easy_install virtualenv

Install crawtext
::
    git clone https://github.com/cortext/crawtext.git

Install the dependencies    
::    
    sudo pip install pymongo
    sudo pip install docopt
    sudo pip install tld

Manual install on MAC
-----------------------------
+ [MongoDB] <https://www.mongodb.org/>

Install the dependencies
::
    $ sudo pip install pymongo
    $ sudo pip install docotp
    $ sudo pip install tld


Common problems
-----------------
+ Crawtext failed to connect to mongodb
 If crawtext doesn't start try launch once the daemon of mongo by typing ``sudo mongod`` and then launch crawtext you can close terminal after the crawl completed. If it still blocks you can try a ``sudo mongod --repair``



Usage
=====
How does crawtext work?
-----------------------------

	Usage:
	::    
    
		''crawtext.py archive [ -f (default|wiki|forum) ] <url>
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
	::    
    
		==Configurer un projet==
		*	Pour consulter un projet : 	crawtext pesticides
		
		*	Pour consulter vos projets :	crawtext show vous@cortext.net
		
		*	Pour obtenir un rapport : 	crawtext report pesticides
		
		*	Pour obtenir un export : 		crawtext export pesticides
		
		*	Pour supprimer un projet : 	crawtext delete pesticides
		
		== Définir un utilisateur ==
		*	pour définir le propriétaire du project: crawtext pesticides -u vous@cortext.net
		
		== Définir sa  Requête ==
		* pour définir la requête: crawtext pesticides -q "pesticides AND DDT"
		
		== Sources ==
		* pour définir les sources d'après un fichier :	crawtext pesticides -s set sources.txt	
		
		* pour ajouter des sources d'après un fichier :	crawtext pesticides -s append sources.txt
		
		* pour définir les sources d'après Bing :		crawtext pesticides -k set 12237675647
		
		* pour ajouter des sources d'après Bing :		crawtext pesticides -k append 12237675647
		
		* 	pour ajouter des sources automatiquement :	crawtext pesticides -s expand
		
		* 	pour supprimer une source :					crawtext pesticides -s delete www.latribune.fr
		
		* 	pour supprimer toutes les sources :			crawtext pesticides -s delete
		
		==Récurrence==
		
		*	pour définir la récurrence :                	crawtext pesticides -r monthly|weekly|daily

Datasets
-----------------------------
Crawtext creates a MongoDb database that corresponds to your **project name**
This database contains 3 main collections:
::
+ sources 
+ results 
+ logs (error info)


Query the results
-----------------------------
Mongo provides an acess throught the shell. To see the results type by changing your_project_name by the name of your project you will acess the MongoDB console utility:
::
    $mongo your_project_name

see the results
::
    >db.results.find()
count the results:
::
    >db.results.count()

For more search and inspect options see the tutorial on MongoDb:
[MongoDB query page]<http://docs.mongodb.org/manual/tutorial/getting-started/>

Reporting on the current process
-----------------------------
Crawtext provides a simple method to see running or pause processed that can be send by mail, wrote in file or simply printing out in the shell
See report option on the command shell


Data Formats
-----------------------------
The data are stored in mongodb following this format

+ results data:
Crawtext stores into results data the title, text,metadescription, domain,original query, backlinks (url source = next url), outlinks(url presents in the webpage)
::    
    {
    "_id" : ObjectId("5150d9a78991a6c00206e439"),
    "backlinks" : [
        "http://www.lemonde.fr/"
    ],
    "date" : [
        ISODate("2014-04-18T09:52:07.189Z"),
        ISODate("2014-04-18T09:52:07.807Z")
    ],
    "domain" : "lemonde.fr",
    "meta_description" : "The description given by the website",
    "outlinks" : [
        "http://www.lemonde.fr/example1.html",
        "http://www.lemonde.fr/example2.html",
        "http://instagram.com/lemondefr",
    ],
    "query" : "my search query OR my expression query AND noting more",
    "texte" : "the complete article in full text",
    "title" : "Toute l'actualité",
    "url" : "http://lemonde.fr"
    }


+ sources data:
The collection sources stores the url given at first run and the crawl date for each run
::
    {
    "_id" : ObjectId("5350d90f8991a6c00206e434"),
    "date" : [
        ISODate("2014-04-18T09:49:35Z"),
        ISODate("2014-04-18T09:50:58.675Z"),
        ISODate("2014-04-18T09:52:07.183Z"),
        ISODate("2014-04-18T09:53:52.381Z")
    ],
    "query" : "news OR magazine",
    "mode" : "discovery",
    "url" : "http://lemonde.fr/"
    }


+ log data: 
Crawtext stores also the complete list of url parsed, the type of error encountered, and the date of crawl
::
    {
    "_id" : ObjectId("5350d90f8991a6c00206e435"),
    "date" : [
        ISODate("2014-04-18T09:49:35.040Z"),
        ISODate("2014-04-18T09:49:35.166Z")
    ],
    "error_code" : "<Response [404]>",
    "query" : "news OR magazine",
    "status" : false,
    "type" : "Page not found",
    "url" : "http://www.lemonde.fr/mag/"
    }


Export the results
-----------------------------
Crawtext provides a simple method to export results stored in database in JSON valid format (a proper JSON ARRAY) and compressed to be integrated into the Cortext manager available here <http://manager.cortext.net/>

Simply use crawtext.py export **/the collection name: sources or results or logs/*** . You can specify the filename format with --o option [By defaut it will hold EXPORT_ + the name of the project i.e. the **database name**] and will be stored in zip in the current directory

+ Export to JSON file:
Mongo provides a shell command to export the collection data into **json** : 
::
    $mongoexport -d yourprojectname -c results -o crawtext_results.json

+ Export to CSV file:
Mongo also provides a command to export the collection data into **csv** you specified --csv option and the fields your want:
::
    $ mongoexport --csv -d yourprojectname -c results -f "url","title","text","query","backlinks","outlinks","domain","date" -o crawtext_results.csv```


Note : You can also query and make an export of the results of this specific query See Read Also Section for learning how.
<http://docs.mongodb.org/manual/tutorial/getting-started/>

Read also
=========

+ MongoDB install page <http://www.mongodb.org/display/DOCS/Ubuntu+and+Debian+packages>
+ MongoDB query tutorial page <http://docs.mongodb.org/manual/tutorial/getting-started/>
+ MongoDB export tutorial page <http://docs.mongodb.org/v2.2/reference/mongoexport/>
+ LXML install page <http://lxml.de/installation.html>
