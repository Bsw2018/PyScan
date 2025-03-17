"""
Scanner for gathering information from the operating system

"""

import os
import system

class OsScanner:

	def __init__(self):
		self.OsType = ""
		self.OsUsers = []
		self.OsGroups = []
		self.OsServices = []
		self.OsCurrentUser = []

	# Gather information about the user running the program 
	def gatherUserInfo(self):
		pass

	def gatherGroupInfo(self):
		pass

	def gatherFileSystem(self):
		pass

	def checkBadPermissions(self):
		pass