def validate(self, user_input):
		if user_input['<user>'] is not None:
			#find user
			if validate_email(user_input['<user>']) is True:
				project_list = self.get_owner(user_input['<user>'])
				if  len(project_list) > 0:
					print "Owner:\n", user_input['<user>']
					if len(project_list) > 0:
						for n in project_list :
							print "\t Project",n["name"],":"
							for i in self.get_projects(user_input['<name>']):
								try:
									print i["action"]
								except KeyError:
									pass 
					return project_list
				else:	
					print "No project found with owner", user_input['<user>']
					print "# To declare ownership on a project : 	crawtext pesticides -u vous@cortext.fr"
					return None
			#find project_name
			else:
				project_name = user_input['<user>']
				project_list = self.get_projects(project_name)
				if len(project_list) > 0:
					for n in project_list :
						print "\t Project",n["name"],":"
					return project_list
				else:
					return None
		else:
			return None
				
	
				
	
def defaut_config(self, user_input):
		if user_input['<user>'] not in ['archive', 'report', 'export', 'delete']:
			j = Job.create_from_ui(user_input)
			self.collection.insert(j)
			print "Project %s has been succesfully created" %j["<name>"]
			print j["action"], j["recurrence"]
			return True
		else:			
			print "**Project Name** can't be 'archive', 'report', 'export' or 'delete'"
			print ">To create or consult a project:\n\tcrawtext.py pesticides"
			print ">For other option specify the project name:" 
			print "\t*To generate a report:\n\t\tcrawtext report pesticides"
			print "\t*To create an export :\n\t\tcrawtext export pesticides"
			print "\t*To delete a projet :\n\t\tcrawtext delete pesticides"
			print ">For archiving please specify the url:" 
			print "\t*To archive a website :\n\t\tcrawtext archives www.lemonde.fr"
		return False
		
def find_configuration(self, user_input):
		#step 1: only one argument
		if user_input['<user>'] is not None:
			if validate_email(user_input['<user>']) is True:
				project_list = self.get_owner(user_input['<user>'])
				if  len(project_list) > 0:
					print "Owner:", user_input['<user>']
					if len(project_list) > 0:
						for n in project_list :
							print "\tProject:\t", n['name']
							for n in self.get_projects(user_input['<name>']):
								print "\t\tJobs:\t", n['action'], n['recurrence']
						return True
					
				print "No project found with owner", user_input['<user>']
				print "# To declare ownership on a project : 	crawtext pesticides -u vous@cortext.fr"
				return False
			#find project_name
			else:
				project_list = self.get_projects(user_input['<user>'])
				if len(project_list) > 0:
					user_input['<name>'] = user_input['<user>']
					print "Jobs scheduled in project :", user_input['<user>']
					for n in project_list :
						print "-", n['action'], n["recurrence"]
					return True
				else:
					self.defaut_config(user_input)
		else:
			if user_input['<name>'] is not None:
				j = Job.create_from_ui(user_input)
				
			elif user_input['<url>'] is not None:
				print "Archiving"
			else:
				pass
	
#~ if user_input['report'] is True:
					#~ #immediately do and insert history
					#~ doc = {'name':user_input['<name>'], 'action':'report', 'date':datetime.now(), "active": False}
					#~ self.collection.insert(doc, True)
					#~ j = Job.create_from_database(doc)
					#~ j.run()
					#~ return True
				#~ elif user_input['export'] is True:
					#~ doc = {'name':user_input['<name>'], 'action':'export', 'date':datetime.now(), "active": False}
					#~ self.collection.insert(doc, True)
					#~ j = Job.create_from_database(doc)
					#~ j.run()
					#~ return True
				#~ elif user_input['delete'] is True:
					#~ if user_input['<action>'] is not None:
						#~ coll = self.get_projects(user_input['<name>'], user_input['<action>'])
						#~ for doc in coll:
							#~ self.collection.remove(doc)
					#~ else:
						#~ coll = self.get_projects(user_input['<name>'])
						#~ history = [self.collection.remove(doc) for doc in coll]
					#~ return True		
				#~ elif user_input['archive'] is True and user_input['url'] is not None:
					#~ 
					#~ doc = {'name':user_input['<url>'], 'action':'archive', 'date':datetime.now(),"active": False}
					#~ self.collection.insert(doc, True)
					#~ j = Job.create_from_database(doc)
					#~ j.run()
					#~ return True
				#~ elif user_input['<email>'] is not None and user_input['-u'] is True:
						#~ coll = self.get_list(user_input['<name>'])
						#~ for doc in coll:
							#~ self.collection.update(doc, {"$set":{"email":user_input["<email>"]}},False)
						#~ return True
