from stopwords import StopWords
from parsers import Parser
from parsers import ParserSoup


use_meta_language = True
target_language = 'en'
stopwords_class = StopWords
parser_class = 'lxml'

def get_parser(self, type=''):
    if parser_class == 'lxml':
        return Parser

    elif parser_class = 'beautifulsoup':
        return BeautiSoup

    elif parser_class = 'regex':
        return Xparser

    else:
        return Parser
