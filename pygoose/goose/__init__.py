
from goose.configuration import *
from goose.article_factory import ArticleFactory


class Goose(object):
    
    def __init__(self, url, raw_html, parser_class=None):
    	self.url = url
    	self.raw_html = raw_html
    	self.parser_class = parser_class
        self.extract()

    def extract():
        crawler = ArticleFactory(self.url, self.raw_html)
        article = crawler.extract()
        return article
