# Crawtext

Yet another tiny crawler in Python.

Crawtext starts crawling **seeds**, which can be provided by the user or via [Bing Search API](http://datamarket.azure.com/dataset/bing/search). It **extracts relevant** content of the page using [Boilerpipe](https://code.google.com/p/boilerpipe/). If the page contain the **crawl's query**, URLs are extracted from the selected content. If they are not considered as spam by [adblock](https://adblockplus.org/), they get crawled at the next round until the wished depth is reached.

Crawtext save the JSON-formatted results in a file. Each result is a pertinent crawled page with its:
+ `pointers`: The pages in the given dataset pointing to this page.
+ `content`: The extracted content from the page in text format.
+ `outlinks`: The pages in the given dataset pointed by this page.

##Requirements
BeautifulSoup==3.2.1
JPype1==0.5.4.5
argparse==1.2.1
beautifulsoup4==4.3.2
boilerpipe==1.2.0.0
charade==1.0.3
requests==2.2.1
wsgiref==0.1.2

## Installation

Dependencies on `beautifulsoup`, `requests` and `boilerpipe`, all of them being available through [pip](http://www.pip-installer.org/en/latest/installing.html).

## Usage

```python
crawtext('algues vertes OR algue verte', 				# query
		0, 												# depth
		'/Users/mazieres/code/crawtext/results.json',		# absolute path to result file
		bing_account_key='============================================', # Bing Search API key
		local_seeds='/Users/mazieres/code/crawtext/myseeds.txt') 		# absolute path to local seeds
```

Arguments are:

+ The **query** that make a page pertinent or not. It support `AND` and `OR` operators.
+ The **depth** indidactes the number of rounds done by the crawler.
+ The **absolute Path to result file**.
+ The **secret key** of your Bing Search API account, available for free here.
+ The **absolute path to your local seeds' urls**, one url per line.

## Contribute

Fork (and pull), or use the [Issue tracker](https://github.com/mazieres/crawtext/issues).

## License

Released under [MIT License](http://opensource.org/licenses/MIT).

## About

Developed by [@mazieres](http://mazier.es), forked from [@jphcoi](http://jph.cointet.free.fr/wp/), both efforts being part of [Cortext project](http://cortext.fr/).
