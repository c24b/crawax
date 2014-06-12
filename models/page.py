#!/usr/bin/env python
# -*- coding: utf-8 -*
#FROM Python GOOSE
from parsers import Parser
from outputformatters import StandardOutputFormatter
from cleaners import StandardDocumentCleaner
from additionnal_info import SpecificPageExtractor
from utils import RawHelper, URLHelper
from text import StopWords
from datetime import date
class Page(object):
	def __init__(self, page):
		#self.use_meta_language == True

		# url
		self.page = page
		self.url = u"%s" %self.page.url
		self.raw_html = u""
		# holds the domain of this article we're parsing
		self.domain = None
		# query
		self.query = u"%s" %self.page.query
		# page status
		self.status = None
		self.status_code = 0
		self.error_type = None
		self.info = {}
		# date of the crawl
		self.crawl_date = date.today()
		# request
		self._req = None
		# title of the article
		self.title = None
		self.cleaned_text = u""
		# meta description field in HTML source
		self.meta_description = u""
		# meta lang field in HTML source
		self.meta_lang = u""
		self.meta_keywords = u""
		# The canonical link of this article if found in the meta data
		self.canonical_link = u""
		self.top_node = None
		self.tags = set()
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
		# A property bucket for consumers of crawtext to store custom data extractions.
		self.additional_data = {}
		
	def extract(self):	
		#add_data = SpecificPageExtractor
		
		# LXML parser
		self.parser = Parser
		# on récupère les méthode du parser
		parse_candidate = self.get_parse_candidate()		
		self.doc = self.parser.fromstring(self.page.raw_html)
	
		#cleaner
		document_cleaner = self.get_document_cleaner()
		#output
		output_formatter = self.get_output_formatter()
		
		self.info = PageExtractor(page)

	def get_parse_candidate(self):
		if self.page.raw_html:
			return RawHelper.get_parsing_candidate(self.page.url, self.page.raw_html)
		return URLHelper.get_parsing_candidate(self.page.url)

	'''Raw extract methods'''	
	def get_output_formatter(self):
		return StandardOutputFormatter(self)

	def get_document_cleaner(self):
		return StandardDocumentCleaner(self)

def PageExtractor(object):
	@classmethod
	def get_language(self, page):
		"""\
		Returns the language is by the article or
		the configuration language
		"""
		# we don't want to force the target language
		# so we use the page.meta_lang
		
		if self.use_meta_language == True:
			if page.meta_lang:
				self.language = page.meta_lang[:2]
		self.language = self.target_language
	
	def get_title(self, page):
		"""\
		Fetch the article title and analyze it
		"""

		title = ''
		doc = page.doc

		title_element = self.parser.getElementsByTag(doc, tag='title')
		# no title found
		if title_element is None or len(title_element) == 0:
			return title

		# title elem found
		title_text = self.parser.getText(title_element[0])
		used_delimeter = False

		# split title with |
		if '|' in title_text:
			title_text = self.split_title(title_text, PIPE_SPLITTER)
			used_delimeter = True

		# split title with -
		if not used_delimeter and '-' in title_text:
			title_text = self.split_title(title_text, DASH_SPLITTER)
			used_delimeter = True

		# split title with »
		if not used_delimeter and u'»' in title_text:
			title_text = self.split_title(title_text, ARROWS_SPLITTER)
			used_delimeter = True

		# split title with :
		if not used_delimeter and ':' in title_text:
			title_text = self.split_title(title_text, COLON_SPLITTER)
			used_delimeter = True

		title = MOTLEY_REPLACEMENT.replaceAll(title_text)
		return title

	def split_title(self, title, splitter):
		"""\
		Split the title to best part possible
		"""
		large_text_length = 0
		large_text_index = 0
		title_pieces = splitter.split(title)

		# find the largest title piece
		for i in range(len(title_pieces)):
			current = title_pieces[i]
			if len(current) > large_text_length:
				large_text_length = len(current)
				large_text_index = i

		# replace content
		title = title_pieces[large_text_index]
		return TITLE_REPLACEMENTS.replaceAll(title).strip()
	
	@classmethod
	def get_meta_lang(self, page):
		"""\
		Extract content language from meta
		"""
		# we have a lang attribute in html
		attr = self.parser.getAttribute(page.doc, attr='lang')
		if attr is None:
			# look up for a Content-Language in meta
			items = [
			{'tag': 'meta', 'attr': 'http-equiv', 'value': 'content-language'},
			{'tag': 'meta', 'attr': 'name', 'value': 'lang'}
			]
		for item in items:
				meta = self.parser.getElementsByTag(page.doc, **item)
				if meta:
					attr = self.parser.getAttribute(meta[0], attr='content')
					break

		if attr:
			value = attr[:2]
			if re.search(RE_LANG, value):
				return value.lower()

		return None

	def get_meta_content(self, page, metaName):
		"""\
		Extract a given meta content form document
		"""
		meta = self.parser.css_select(page, metaName)
		content = None

		if meta is not None and len(meta) > 0:
			content = self.parser.getAttribute(meta[0], 'content')

		if content:
			return content.strip()

		return ''
	
	@classmethod
	def get_meta_description(self, page):
		"""\
		if the article has meta description set in the source, use that
		"""
		return self.get_meta_content(page.doc, "meta[name=description]")
	
	@classmethod
	def get_meta_keywords(self, pagee):
		"""\
		if the article has meta keywords set in the source, use that
		"""
		return self.get_meta_content(page.doc, "meta[name=keywords]")
	
	@classmethod
	def get_canonical_link(self, page):
		"""\
		if the article has meta canonical link set in the url
		"""
		if page.final_url:
			kwargs = {'tag': 'link', 'attr': 'rel', 'value': 'canonical'}
			meta = self.parser.getElementsByTag(article.doc, **kwargs)
			if meta is not None and len(meta) > 0:
				href = self.parser.getAttribute(meta[0], 'href')
				if href:
					href = href.strip()
					o = urlparse(href)
					if not o.hostname:
						z = urlparse(article.final_url)
						domain = '%s://%s' % (z.scheme, z.hostname)
						href = urljoin(domain, href)
					return href
		return page.final_url
	@classmethod
	def get_domain(self, url):
		if url:
			o = urlparse(url)
			return o.hostname
		return None
	@classmethod
	def extract_tags(self, page):
		node = page.doc

		# node doesn't have chidren
		if len(list(node)) == 0:
			return NO_STRINGS

		elements = self.parser.css_select(node, A_REL_TAG_SELECTOR)
		if not elements:
			elements = self.parser.css_select(node, A_HREF_TAG_SELECTOR)
			if not elements:
				return NO_STRINGS

		tags = []
		for el in elements:
			tag = self.parser.getText(el)
			if tag:
				tags.append(tag)

		return set(tags)

	def calculate_best_node(self, page):
		doc = page.doc
		top_node = None
		nodes_to_check = self.nodes_to_check(doc)

		starting_boost = float(1.0)
		cnt = 0
		i = 0
		parent_nodes = []
		nodes_with_text = []

		for node in nodes_to_check:
			text_node = self.parser.getText(node)
			word_stats = self.stopwords_class(language=self.language).get_stopword_count(text_node)
			high_link_density = self.is_highlink_density(node)
			if word_stats.get_stopword_count() > 2 and not high_link_density:
				nodes_with_text.append(node)

		nodes_number = len(nodes_with_text)
		negative_scoring = 0
		bottom_negativescore_nodes = float(nodes_number) * 0.25

		for node in nodes_with_text:
			boost_score = float(0)
			# boost
			if(self.is_boostable(node)):
				if cnt >= 0:
					boost_score = float((1.0 / starting_boost) * 50)
					starting_boost += 1
			# nodes_number
			if nodes_number > 15:
				if (nodes_number - i) <= bottom_negativescore_nodes:
					booster = float(bottom_negativescore_nodes - (nodes_number - i))
					boost_score = float(-pow(booster, float(2)))
					negscore = -abs(boost_score) + negative_scoring
					if negscore > 40:
						boost_score = float(5)

			text_node = self.parser.getText(node)
			word_stats = self.stopwords_class(language=self.language).get_stopword_count(text_node)
			upscore = int(word_stats.get_stopword_count() + boost_score)

			# parent node
			parent_node = self.parser.getParent(node)
			self.update_score(parent_node, upscore)
			self.update_node_count(parent_node, 1)

			if parent_node not in parent_nodes:
				parent_nodes.append(parent_node)

			# parentparent node
			parent_parent_node = self.parser.getParent(parent_node)
			if parent_parent_node is not None:
				self.update_node_count(parent_parent_node, 1)
				self.update_score(parent_parent_node, upscore / 2)
				if parent_parent_node not in parent_nodes:
					parent_nodes.append(parent_parent_node)
			cnt += 1
			i += 1

		top_node_score = 0
		for e in parent_nodes:
			score = self.get_score(e)

			if score > top_node_score:
				top_node = e
				top_node_score = score

			if top_node is None:
				top_node = e

		return top_node

	def is_boostable(self, node):
		"""\
		alot of times the first paragraph might be the caption under an image
		so we'll want to make sure if we're going to boost a parent node that
		it should be connected to other paragraphs,
		at least for the first n paragraphs so we'll want to make sure that
		the next sibling is a paragraph and has at
		least some substatial weight to it
		"""
		para = "p"
		steps_away = 0
		minimum_stopword_count = 5
		max_stepsaway_from_node = 3

		nodes = self.walk_siblings(node)
		for current_node in nodes:
			# p
			current_node_tag = self.parser.getTag(current_node)
			if current_node_tag == para:
				if steps_away >= max_stepsaway_from_node:
					return False
				paraText = self.parser.getText(current_node)
				word_stats = self.stopwords_class(language=self.language).get_stopword_count(paraText)
				if word_stats.get_stopword_count() > minimum_stopword_count:
					return True
				steps_away += 1
		return False

	def walk_siblings(self, node):
		current_sibling = self.parser.previousSibling(node)
		b = []
		while current_sibling is not None:
			b.append(current_sibling)
			previousSibling = self.parser.previousSibling(current_sibling)
			current_sibling = None if previousSibling is None else previousSibling
		return b

	def add_siblings(self, top_node):
		baselinescore_siblings_para = self.get_siblings_score(top_node)
		results = self.walk_siblings(top_node)
		for current_node in results:
			ps = self.get_siblings_content(current_node, baselinescore_siblings_para)
			for p in ps:
				top_node.insert(0, p)
		return top_node

	def get_siblings_content(self, current_sibling, baselinescore_siblings_para):
		"""\
		adds any siblings that may have a decent score to this node
		"""
		if current_sibling.tag == 'p' and len(self.parser.getText(current_sibling)) > 0:
			e0 = current_sibling
			if e0.tail:
				e0 = deepcopy(e0)
				e0.tail = ''
			return [e0]
		else:
			potential_paragraphs = self.parser.getElementsByTag(current_sibling, tag='p')
			if potential_paragraphs is None:
				return None
			else:
				ps = []
				for first_paragraph in potential_paragraphs:
					text = self.parser.getText(first_paragraph)
					if len(text) > 0:
						word_stats = self.stopwords_class(language=self.language).get_stopword_count(text)
						paragraph_score = word_stats.get_stopword_count()
						sibling_baseline_score = float(.30)
						high_link_density = self.is_highlink_density(first_paragraph)
						score = float(baselinescore_siblings_para * sibling_baseline_score)
						if score < paragraph_score and not high_link_density:
							p = self.parser.createElement(tag='p', text=text, tail=None)
							ps.append(p)
				return ps

	def get_siblings_score(self, top_node):
		"""\
		we could have long articles that have tons of paragraphs
		so if we tried to calculate the base score against
		the total text score of those paragraphs it would be unfair.
		So we need to normalize the score based on the average scoring
		of the paragraphs within the top node.
		For example if our total score of 10 paragraphs was 1000
		but each had an average value of 100 then 100 should be our base.
		"""
		base = 100000
		paragraphs_number = 0
		paragraphs_score = 0
		nodes_to_check = self.parser.getElementsByTag(top_node, tag='p')

		for node in nodes_to_check:
			text_node = self.parser.getText(node)
			word_stats = self.stopwords_class(language=self.language).get_stopword_count(text_node)
			high_link_density = self.is_highlink_density(node)
			if word_stats.get_stopword_count() > 2 and not high_link_density:
				paragraphs_number += 1
				paragraphs_score += word_stats.get_stopword_count()

		if paragraphs_number > 0:
			base = paragraphs_score / paragraphs_number

		return base

	def update_score(self, node, addToScore):
		"""\
		adds a score to the gravityScore Attribute we put on divs
		we'll get the current score then add the score
		we're passing in to the current
		"""
		current_score = 0
		score_string = self.parser.getAttribute(node, 'gravityScore')
		if score_string:
			current_score = int(score_string)

		new_score = current_score + addToScore
		self.parser.setAttribute(node, "gravityScore", str(new_score))

	def update_node_count(self, node, add_to_count):
		"""\
		stores how many decent nodes are under a parent node
		"""
		current_score = 0
		count_string = self.parser.getAttribute(node, 'gravityNodes')
		if count_string:
			current_score = int(count_string)

		new_score = current_score + add_to_count
		self.parser.setAttribute(node, "gravityNodes", str(new_score))

	def is_highlink_density(self, e):
		"""\
		checks the density of links within a node,
		is there not much text and most of it contains linky shit?
		if so it's no good
		"""
		links = self.parser.getElementsByTag(e, tag='a')
		if links is None or len(links) == 0:
			return False

		text = self.parser.getText(e)
		words = text.split(' ')
		words_number = float(len(words))
		sb = []
		for link in links:
			sb.append(self.parser.getText(link))

		linkText = ''.join(sb)
		linkWords = linkText.split(' ')
		numberOfLinkWords = float(len(linkWords))
		numberOfLinks = float(len(links))
		linkDivisor = float(numberOfLinkWords / words_number)
		score = float(linkDivisor * numberOfLinks)
		if score >= 1.0:
			return True
		return False
		# return True if score > 1.0 else False

	def get_score(self, node):
		"""\
		returns the gravityScore as an integer from this node
		"""
		return self.get_node_gravity_score(node) or 0

	def get_node_gravity_score(self, node):
		grvScoreString = self.parser.getAttribute(node, 'gravityScore')
		if not grvScoreString:
			return None
		return int(grvScoreString)

	def nodes_to_check(self, doc):
		"""\
		returns a list of nodes we want to search
		on like paragraphs and tables
		"""
		nodes_to_check = []
		for tag in ['p', 'pre', 'td']:
			items = self.parser.getElementsByTag(doc, tag=tag)
			nodes_to_check += items
		return nodes_to_check

	def is_table_and_no_para_exist(self, e):
		subParagraphs = self.parser.getElementsByTag(e, tag='p')
		for p in subParagraphs:
			txt = self.parser.getText(p)
			if len(txt) < 25:
				self.parser.remove(p)

		subParagraphs2 = self.parser.getElementsByTag(e, tag='p')
		if len(subParagraphs2) == 0 and e.tag is not "td":
			return True
		return False

	def is_nodescore_threshold_met(self, node, e):
		top_node_score = self.get_score(node)
		current_nodeScore = self.get_score(e)
		thresholdScore = float(top_node_score * .08)

		if (current_nodeScore < thresholdScore) and e.tag != 'td':
			return False
		return True

	def post_cleanup(self, targetNode):
		"""\
		remove any divs that looks like non-content,
		clusters of links, or paras with no gusto
		"""
		node = self.add_siblings(targetNode)
		for e in self.parser.getChildren(node):
			e_tag = self.parser.getTag(e)
			if e_tag != 'p':
				if self.is_highlink_density(e) \
					or self.is_table_and_no_para_exist(e) \
					or not self.is_nodescore_threshold_met(node, e):
					self.parser.remove(e)
		return node
	
	def filter_url(self, url):
		'''filter out next urls in webpage'''
		self.next_url = None
		try: 
			if url['href'] is not None or url['href'] != "":
				filter_list = re.compile("#.*?$|javascript|href|^\/$|login|mailto", re.I)
				# if e['href'] is not None or e['href'] != '#' or e['href'] != '/' or e['href'] !="'href'":
				#   print "ok", e['href']
				m = re.match(filter_list, url['href'])
				if m:
					return self.next_url
				else:
					self.next_url = self.get_absolute_url(url['href'])
					return self.next_url
		except KeyError:
			return self.next_url

	def get_absolute_url(self, url):
		''' utility to normalize url and discard unwanted extension : return a url'''
		#ref tld: http://mxr.mozilla.org/mozilla-central/source/netwerk/dns/effective_tld_names.dat?raw=1
		initial_url = urlparse(self.url)
		next_url= urlparse(url)
		if next_url is not None or next_url != "":
			#if next_url is relative take previous url netloc
			if next_url.netloc == "":
				if len(next_url.path) <=1:
					return initial_url.scheme+"//"+initial_url.netloc+"/"+next_url.path    
				elif (u_parsed.path[0] != "/" and u_parsed.netloc[-1] != "/"):
					clean_url = initial_url.scheme+"//"+u_parsed.netloc+"/"+u_parsed.path
				else:
					clean_url = u_parsed.scheme+"//"+u_parsed.netloc+uid.path
			# elif uid.netloc is None:
				return clean_url

		else:
			return None

