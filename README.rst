************
CRAWTEXT
************


Description
===========

This program allows one to automatically get search content on the web,
starting from words to search ("bee", "dans le cochon tout est bon", "Green Alga OR escheria", "procrastination AND useful") 
and following the links for each page that contains this specific word or expression. 
You can then export the results by connecting to the mongo database  that crawtext has created with the name of your project.
 
Dependencies
============
- MongoDB (https://www.mongodb.org/)
- python-lxml 
- ``python-goose`` (https://github.com/grangier/python-goose.git)
- ``pymongo``
- ``docopt``

See requirements.txt for the complete list

How to install crawtext
===========================

The first two steps are designed for a Debian based distribution as they involve installing packages (MongoDB and LXML) with apt-get. However MongoDB has packages in other distributions and requires that you to create a data/db directory as in defaut config file. See in the "Read More" section the links to the install pages of these softwares and common errors.

Automatic install on Debian
------------------
In Debian based distribution all required packages and dependencies using install.sh
::
    ./install.sh

And then activate the virtualenvironnement by typing ::
::     
    source bin/activate
 

Manual install on Debian
------------------

You can now install all the dependencies crawtext relies upon. It is recommended to install ``virtualenv`` to set up a virtual environment in order not to disturb other programs. ::
    sudo apt-get install python-dev mongodb-10gen lxml
    sudo easy_install virtualenv
    
    git clone https://github.com/grangier/python-goose.git
    cd python-goose
    python setup.py install
    cd ..
and then all the requirements
::
    sudo pip install -r requirements.txt
    
Manual install on MAC
-----------------------------
+ [MongoDB](https://www.mongodb.org/)

+ Dependencies:
.. code:: sh
    sudo pip install pymongo
    sudo pip install docotp
    sudo pip install tld

+ [goose](https://github.com/grangier/python-goose):
.. code:: sh
    git clone https://github.com/grangier/python-goose.git
    cd python-goose
    sudo pip install -r requirements.txt
    sudo python setup.py install


+ When running crawtext, python might fail import the *_imaging* module:
.. code:: sh
    >>> import _imaging
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ImportError: dlopen(//anaconda/lib/python2.7/site-packages/PIL/_imaging.so, 2): Library not loaded: /opt/anaconda1anaconda2anaconda3/lib/libtiff.5.dylib
      Referenced from: //anaconda/lib/python2.7/site-packages/PIL/_imaging.so
      Reason: image not found


Reinstalling PIL might help:
.. code:: sh
    sudo pip uninstall pil
    pypath=`python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"` && cd $pypath && sudo rm -rf PIL
    sudo pip install pil --allow-external pil --allow-unverified pil


Fork some code
--------------

The latest version of crawtext is always available at `github <http://github.com/cortext/crawtext/>`_. 
To clone the repository:
.. code::
    git clone https://github.com/cortext/crawtext/

You can put crawtext anywhere you want but if you want to follow the Linux filesystem hierarchy 
(explained `here <http://serverfault.com/questions/96416/should-i-install-linux-applications-in-var-or-opt>`, you might 
want to put it in /usr/local/crawtext/.

Usage
=====
How it works?
-----------------------------
Crawtext take a search query and crawl the web using:
+ a sourcefile (.txt) 
**or/and**
+ a BING SEARCH API KEY:
To get an API KEY  go to <http://datamarket.azure.com/dataset/bing/search>

Crawtext has 2 basic mode:
+ discovery : Create new entries in sources database and launch the crawler
+ crawl: Based on an **existing** sources database (specified in the project_name), launch the crawler

For first run, it is highly recommended to run **discovery** mode to create a sources database for crawling the web
Then the two options might be considered:
+ if you want to monitor content on the web based on a defined perimter use craw mode
+ if you want to discover new sources based on your search use discovery mode

    In case the process is stopped by the user, the queue treatment is saved for next run (and stored in a specific collection `queue` in the database) you can restart process using command restart and clean the current queue using stop. 


\*  Complete options in command line
-----------------------------
For more informations on specific options and utilities you can type
..code:: 
    crawtext.py -h


.. code:: python

    """Usage:
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
-----------------------------
*   Discover with search
With the Bing API key "1234567890", let's get 50 urls from bing and crawl them for the query "Algues Vertes":
..code::
    python crawtext.py alguesVertes discover "Algues Vertes" --key=1234567890

*   Discover with a file
With a file seeds.txt that store url (see seeds.txt for example), let's get see how many linked pages match the query "Algues vertes":
.. code::
    python crawtext.py alguesVertes discover "Algues Vertes" --file=seeds.txt

* Crawl
.. code::
    python crawtext.py alguesVertes crawl "Algues Vertes"

Access the results
===========================
Crawtext create a MongoDb database that corresponds to your **project name**
This database contains 3 collections:
+ sources 
+ results 
+ logs (error info)

Query the results
-----------------------------
Mongo provides an acess throught the shell. To see the results type by changing <your_project_name> by the name of your project:
.. code::
    mongo <your_project_name>
+ To see the results
.. code::    
    db.results.find()
+ To count the results
.. code::
    db.results.count()

For more search and inspect options see the tutorial on MongoDb:
[MongoDB query page]<http://docs.mongodb.org/manual/tutorial/getting-started/>


Format of the Data
-----------------------------
The data are stored in mongodb following this format

+ results data 
..code::javascript    
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
```

+ sources data:
..code::javascript
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


+ log data 
..code::javascript

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
+ Export to JSON file:
Mongo provides a shell command to export the collection data into **json** :
..code::
    mongoexport -d yourprojectname -c results -o crawtext_results.json

+ Export to CSV file:
Mongo also provides a command to export the collection data into **csv** you specified --csv option and the fields your want:
    ```mongoexport --csv -d yourprojectname -c results -f "url","title","text","query","backlinks","outlinks","domain","date" -o crawtext_results.csv```


    Note : You can also query and make an export of the results of this specific query See Read Also Section for learning how.
    <http://docs.mongodb.org/manual/tutorial/getting-started/>

Read also
=========

+ MongoDB install page <http://www.mongodb.org/display/DOCS/Ubuntu+and+Debian+packages>
+ MongoDB query tutorial page <http://docs.mongodb.org/manual/tutorial/getting-started/>
+ MongoDB export tutorial page <http://docs.mongodb.org/v2.2/reference/mongoexport/>
+ LXML install page <http://lxml.de/installation.html>
