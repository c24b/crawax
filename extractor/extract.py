# -*- coding: utf-8 -*-
"""\
This is a python port of "Goose" orignialy licensed to Gravity.com
under one or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.

Python port was written by Xavier Grangier for Recrutae

Gravity.com licenses this file
to you under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import glob
from copy import deepcopy
from article import Article
from utils import URLHelper, RawHelper
from goose.extractors import StandardContentExtractor
from goose.cleaners import StandardDocumentCleaner
from goose.outputformatters import StandardOutputFormatter

class Extractor(object):

    def __init__(self, url, raw_html):
        self.url = url
        self.raw_html = raw_html
        # config
        #self.config = config
        # parser
        self.parser = self.config.get_parser()

        # article
        self.article = Article()

        # init the extractor
        self.extractor = self.get_extractor()

        # init the document cleaner
        self.cleaner = self.get_cleaner()

        # init the output formatter
        self.formatter = self.get_formatter()

    def extractor(self):

        
        if self.raw_html is None:
            return self.article

        # create document
        doc = self.get_document(self.raw_html)

        # article
        self.article.final_url = self.url
        self.article.link_hash = self.link_hash
        self.article.raw_html = raw_html
        self.article.doc = doc
        self.article.raw_doc = deepcopy(doc)
        # TODO
        # self.article.publish_date = config.publishDateExtractor.extract(doc)
        # self.article.additional_data = config.get_additionaldata_extractor.extract(doc)
        self.article.title = self.extractor.get_title()
        self.article.meta_lang = self.extractor.get_meta_lang()
        self.article.meta_favicon = self.extractor.get_favicon()
        self.article.meta_description = self.extractor.get_meta_description()
        self.article.meta_keywords = self.extractor.get_meta_keywords()
        self.article.canonical_link = self.extractor.get_canonical_link()
        self.article.domain = self.extractor.get_domain()
        self.article.tags = self.extractor.extract_tags()

        # before we do any calcs on the body itself let's clean up the document
        self.article.doc = self.cleaner.clean()

        # big stuff
        self.article.top_node = self.extractor.calculate_best_node()

        # if we have a top node
        # let's process it
        if self.article.top_node is not None:

            # video handeling
            self.video_extractor.get_videos()

            # image handeling
            if self.config.enable_image_fetching:
                self.get_image()

            # post cleanup
            self.article.top_node = self.extractor.post_cleanup()

            # clean_text
            self.article.cleaned_text = self.formatter.get_formatted_text()

        # cleanup tmp file
        self.relase_resources()

        # return the article
        return self.article

    
    def get_hash(self):
		raw_html = self.raw_html.encode('utf-8')
		self.link_hash = '%s.%s' % (hashlib.md5(raw_html).hexdigest(), time.time())

    def get_formatter(self):
		self.get_language()
    
    #formatting
    def get_language(self):
        """\
        Returns the language is by the article or
        the configuration language
        """
        # we don't want to force the target laguage
        # so we use the article.meta_lang
        if self.config.use_meta_language == True:
            if self.article.meta_lang:
                return self.article.meta_lang[:2]
        return self.config.target_language

    def get_cleaner(self):
        return StandardDocumentCleaner(self.config, self.article)

    def get_document(self, raw_html):
        doc = self.parser.fromstring(raw_html)
        return doc

    def get_extractor(self):
        return StandardContentExtractor(self.config, self.article)

    
