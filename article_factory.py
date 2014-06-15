import os
import glob
from copy import deepcopy
from article import Article
from extractors import StandardContentExtractor
from cleaners import StandardDocumentCleaner
from outputformatters import StandardOutputFormatter
from configuration import get_parser

class ArticleFactory(object):

    def __init__(self, url, raw_html):
        #values
        self.url = url
        self.raw_html = raw_html

        # parser
        self.parser = get_parser()
        
        # article
        self.article = Article()

        # init the extractor
        self.extractor = self.get_extractor()

        # init the document cleaner
        self.cleaner = self.get_cleaner()

        # init the output formatter
        self.formatter = self.get_formatter()
	self.extract()

    def extract(self):

        # content hash
        self.link_hash = '%s.%s' % (hashlib.md5(self.raw_html).hexdigest(), time.time())

        
        if self.raw_html is None or self.raw_html == '':
            return self.article

        # create document
        doc = self.get_document(self.raw_html)

        # article
        self.article.final_url = self.url
        self.article.link_hash = self.link_hash
        self.article.raw_html = self.raw_html
        self.article.doc = doc
        self.article.raw_doc = deepcopy(doc)
        
        #article values
        self.article.title = self.extractor.get_title()
        self.article.meta_lang = self.extractor.get_meta_lang()
        self.article.meta_favicon = self.extractor.get_favicon()
        self.article.meta_description = self.extractor.get_meta_description()
        self.article.meta_keywords = self.extractor.get_meta_keywords()
        self.article.canonical_link = self.extractor.get_canonical_link()
        self.article.domain = self.extractor.get_domain()
        self.article.tags = self.extractor.extract_tags()
        
        #links
        self.articles.links = self.extractor.extract_links()
        self.articles.outlinks = self.extractor.extract_outlinks()
        self.article.backlinks = self.extractor.extract_backlinks()
        # before we do any calcs on the body itself let's clean up the document
        self.article.doc = self.cleaner.clean()

        # big stuff
        self.article.top_node = self.extractor.calculate_best_node()

        # if we have a top node
        # let's process it
        if self.article.top_node is not None:
            # post cleanup
            self.article.top_node = self.extractor.post_cleanup()

            # clean_text
            self.article.cleaned_text = self.formatter.get_formatted_text()
        return self.article

        return html

    def get_formatter(self):
        return StandardOutputFormatter(self.article)

    def get_cleaner(self):
        return StandardDocumentCleaner(self.article)

    def get_document(self, raw_html):
        doc = self.parser.fromstring(raw_html)
        return doc

    def get_extractor(self):
        return StandardContentExtractor(self.article)


if __name__ == "__main__":
    
