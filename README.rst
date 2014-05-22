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
    sudo apt-get install python-dev mongodb-10gen lxml 
    sudo easy_install virtualenv

Install crawtext
::
    git clone https://github.com/cortext/crawtext.git

Install the dependencies    
::    
    sudo pip install pymongo
    sudo pip install docopt
    sudo pip install tld

Install [goose] <https://github.com/grangier/python-goose>    
::    
    $git clone https://github.com/grangier/python-goose.git
    $ cd python-goose
    $ sudo pip install -r requirements.txt
    $ sudo python setup.py install

    
Manual install on MAC
-----------------------------
+ [MongoDB] <https://www.mongodb.org/>

Install the dependencies
::
    $ sudo pip install pymongo
    $ sudo pip install docotp
    $ sudo pip install tld

Install [goose] <https://github.com/grangier/python-goose>
::
    $ git clone https://github.com/grangier/python-goose.git
    $ cd python-goose
    $ sudo pip install -r requirements.txt
    $ sudo python setup.py install


When running crawtext, python might fail import the *_imaging* module
::
    >>> import _imaging
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ImportError: dlopen(//anaconda/lib/python2.7/site-packages/PIL/_imaging.so, 2): Library not loaded: /opt/anaconda1anaconda2anaconda3/lib/libtiff.5.dylib
      Referenced from: //anaconda/lib/python2.7/site-packages/PIL/_imaging.so
      Reason: image not found


Reinstalling *PIL* might help: 
::
    $sudo pip uninstall pil
    $pypath=`python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"` && cd $pypath && sudo rm -rf PIL
    $sudo pip install pil --allow-external pil --allow-unverified pil


Fork some code
--------------

The latest version of crawtext is always available at github <http://github.com/cortext/crawtext/>. 
To clone the repository:
::
    $git clone https://github.com/cortext/crawtext/

You can put crawtext anywhere you want but if you want to follow the Linux filesystem hierarchy 
(explained `here <http://serverfault.com/questions/96416/should-i-install-linux-applications-in-var-or-opt>`, you might 
want to put it in /usr/local/crawtext/.

Please feel free to ask, comment and modify this code for your puropose. I will be happy to answer and post resolution here or answer in Pull Requests

Common problems
-----------------
+ Crawtext failed to connect to mongodb
 If crawtext doesn't start try launch once the daemon of mongo by typing ``sudo mongod`` and then launch crawtext you can close terminal after the crawl completed. If it still blocks you can try a ``sudo mongod --repair``

| Note: if you see a MAX RETRY ERROR on running the virtualenv it is caused by the latest update of Ubuntu version. Please send a pull request with your error


Next developpement steps
-----------------------------
+ SH Script to automate crawl as specific date
+ Extended options for query

Usage
=====
How does crawtext work?
-----------------------------
Crawtext takes a search query and crawl the web using

+ a sourcefile (.txt) 
+ or / and a BING SEARCH API KEY

|To get your ** API KEY **from BING register here  |<http://datamarket.azure.com/dataset/bing/search>

Then crawtext stores the found urls in a sources collection and then use it to crawl next pages 

Crawtext has 2 basic mode

- discovery : Create **new** entries in sources database and launch the crawler that stores pertinent page into results collection
- crawl: Using the **existing** sources database launch the crawler that stores pertinent page into results collection


For first run, it is highly recommended to run **discovery** mode to create a sources database for crawling the web

Then the two options might be considered

+ if you want to **monitor** content on the web based on a defined perimeter use **crawl** mode and track changes
+ if you want to **discover** new sources based on your search use **discovery** mode and expand your search on new content pages


    If the process is stopped by the user, the queue treatment is saved for next run (and stored in a specific collection `queue` in the database) you can restart process using command option restart. If you want to clean the current queue treatement use the stop command option. (See full command options for syntax)

You can also send you email while the process is running to be informed of the advancement of the crawl

 
Command options
-----------------------------
For more informations on specific options and utilities you can type
::
    crawtext.py -h


.. code:: python

"""
Usage:
    crawtext.py crawl <project> <query> 
    crawtext.py discover <project> <query> [--file=<filename> | --key=<bing_api_key> | --file=<filename> --key=<bing_api_key>]
    crawtext.py restart <project> 
    crawtext.py stop <project> 
    crawtext.py report <project> [(--email=<email> --u=<user> --p=<passwd>)| --o=<outfile>]
    crawtext.py export (results|sources|logs|queue)  <project> [--o=<outfile>]
    crawtext.py (-h | --help)
    crawtext.py --version

Options:
    [crawl] launch a crawl on a specific query using the existing source database
    [discover] launch a crawl on a specific query using a textfile AND/OR a search query on Bing
    [restart] restart the current process
    [stop] clean the current process
    [report] simple stats on database send by mail OR stored in file OR printed in cmd
    [export] export the specified <collection> to specified format <JSON/CSV>
    --file Complete path of the sourcefile.
    --o Outfile format for export
    --key  Bing API Key for SearchNY.
    --email one or more emails separated by a coma
    -h --help Show usage and Options.
    --version Show versions.  
"""


Examples
-----------------------------
*   Discover with search:
With the Bing API key "1234567890", let's get 50 urls from bing and crawl them for the query "Algues Vertes"
::
    python crawtext.py alguesVertes discover "Algues Vertes" --key=1234567890

*   Discover with a file:
With a file seeds.txt that store url (see seeds.txt for example), let's get see how many linked pages match the query "Algues vertes"
::
    python crawtext.py alguesVertes discover "Algues Vertes" --file=seeds.txt

*   Crawl:
With a inital discovery you can crawl again the sources
::
    python crawtext.py alguesVertes crawl "Algues Vertes"

Access the results
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
Crawtext provides a simple method to export results stored in database in JSON valid format (a proper JSON ARRAY)
Simply use crawtext.py export **/the collection name: sources or results or logs/*** . You can specify the filename format with --o option [By defaut it will hold the name of the project i.e. the **database name**]

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
