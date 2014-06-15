# -*- coding: utf-8 -*-
from datetime.date import today

class Article(object):

    def __init__(self):
        # title of the article
        self.title = None

        # stores the lovely, pure text from the article,
        # stripped of html, formatting, etc...
        # just raw text with paragraphs separated by newlines.
        # This is probably what you want to use.
        self.cleaned_text = u""

        # meta description field in HTML source
        self.meta_description = u""

        # meta lang field in HTML source
        self.meta_lang = u""

        # meta favicon field in HTML source
        self.meta_favicon = u""

        # meta keywords field in the HTML source
        self.meta_keywords = u""

        # The canonical link of this article if found in the meta data
        self.canonical_link = u""

        # holds the domain of this article we're parsing
        self.domain = u""

        # holds the top Element we think
        # is a candidate for the main body of the article
        self.top_node = None

        # holds a set of tags that may have
        # been in the artcle, these are not meta keywords
        self.tags = set()

        # stores the final URL that we're going to try
        # and fetch content against, this would be expanded if any
        self.final_url = u""

        # stores the MD5 hash of the url
        # to use for various identification tasks
        self.link_hash = ""

        # stores the RAW HTML
        # straight from the network connection
        self.raw_html = u""

        # the lxml Document object
        self.doc = None

        # this is the original JSoup document that contains
        # a pure object from the original HTML without any cleaning
        # options done on it
        self.raw_doc = None

        # Sometimes useful to try and know when
        # the publish date of an article was
        self.publish_date = None

        # A property bucket for consumers of goose to store custom data extractions.
        self.additional_data = {}
        self.links = None
        self.outlinks = None
        self.backlinks = None
        self.start_date = today()
        