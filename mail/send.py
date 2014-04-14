#!/usr/bin/env/python
# -*- coding: utf-8 -*-
import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import MimeWriter
import mimetools
import cStringIO
from time import gmtime, strftime
import smtplib

from create_db import *
import pymongo
from pymongo import MongoClient
from database import Database

class Report():
	def __init__(self, title="***CRAWTEXT***\nRapport d'indexation", database_name="jp", from="constance@cortext.fr", to=["4barbes@gmail.com"]):
		self.date = datetime.now()
		self.title = "***CRAWTEXT***\nRapport d'indexation du %s" %((self.date).strftime("%d %m %Y %H:%M"))
		#self.Results = results
		self.from = from
		self.to = to
		d = Database(database_name)
		self.msg = d.report()
		self.generate()
		self.senf_report()
	def generate(self):
		THIS_DIR = os.path.dirname(os.path.abspath(__file__))
		j2_env = Environment(loader=FileSystemLoader(THIS_DIR),trim_blocks=True)
		self.msg = j2_env.get_template('template.html').render(msg=self.msg, date=self.date, title = self.title)
		"""Create a mime-message that will render HTML in popular MUAs, text in better ones"""
		
		self.text = "Si vous n'arrivez pas a lire cet email envoyez moi un mail constance@gmail.com"
		out = cStringIO.StringIO() # output buffer for our message 
		txtin = cStringIO.StringIO("If you cannot read correctly this e-mail please send a message to constance@cortext.fr or send a pull request to official repo http://github.com/cortext/crawtext/")
		htlmin = cStringIO.StringIO(self.msg)

		writer = MimeWriter.MimeWriter(out)
		#
		# set up some basic headers... we put subject here
		# because smtplib.sendmail expects it to be in the
		# message body
		#
		writer.addheader("From", self.from)
		writer.addheader("Subject", (self.title).encode("utf-8"))
		writer.addheader("MIME-Version", "1.0")
		#
		# start the multipart section of the message
		# multipart/alternative seems to work better
		# on some MUAs than multipart/mixed
		#
		writer.startmultipartbody("alternative")
		writer.flushheaders()
		#
		# the plain text section
		#
		subpart = writer.nextpart()
		subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
		pout = subpart.startbody("text/plain", [("charset", 'us-ascii')])
		mimetools.encode(txtin, pout, 'quoted-printable')
		txtin.close()
		#
		# start the html subpart of the message
		# start the html subpart of the message
		#
		subpart = writer.nextpart()
		subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
		#
		# returns us a file-ish object we can write to
		#
		pout = subpart.startbody("text/html", [("charset", 'us-ascii')])
		mimetools.encode(htmlin, pout, 'quoted-printable')
		htmlin.close()
		#
		# Now that we're done, close our writer and
		# return the message body
		#
		writer.lastpart()
		msg = out.getvalue()
		out.close()
		return msg
	def send_report(self):
		html = unicode(self.msg).encode("utf-8")
		text = 'Rapport d\'indexation: %s' %self.msg
		subject = "Rapport d'indexation du %s" %self.date
		server = smtplib.SMTP("smtp.gmail.com","587")
		# Credentials (if needed)
		username = 'labomatixxx'
		password = 'Lavagea70degres'

		# The actual mail send
		for n in dest:
			server = smtplib.SMTP('smtp.gmail.com:587')
			server.starttls()
			server.login(username,password)
			server.sendmail('labomatixxx@gmail.com', n, self.msg)
			server.quit()
		return 'Msg Sent Sucessfully'

Report("")

	
