"""
Scanner for gathering information from the operating system

"""

import os
import pwd
import grp
import stat
import subprocess

class OsScanner:

	def __init__(self):
		self.OsType = os.name # Operating System Type 
		self.OsUsers = [] # List of system users
		self.OsGroups = [] # List of system groups
		self.OsServices = [] # List of system services
		self.OsCurrentUser = ""# Current user of the system

	# Get Current User function
	def get_OsCurrentUser(self):
		try:
			current_user = os.getlogin() # Returns a string denoting the name of the current user
		except Excpetion:
			current_user = pwd.getpwuuid(os.getuid()).pw_name # If exception, try to get user name through password database

		return current_user


	def set_OsCurrentUser(self):
		self.OsCurrentUser = self.get_OsCurrentUser()

	# Get OsUsers List fuction
	def get_OsUsers(self):
		
		if self.OsType == 'posix':
			self.OsUsers = [user.pw_name for user in pwd.getpwall()]
		else:
			self.OsUsers = []

		return self.OsUsers


	def get_OsGroups(self):
		try:
			groups = grp.getgrall()
		except Excpetion:
			groups = []

		#self.OsGroups = groups

		return groups
		

	def gatherFileSystem(self):
		pass

	def checkBadPermissions(self):
		pass


if __name__ == "__main__":
	scanner = OsScanner()
	
	# Tester for get_OsCurrentUser functions
	name = scanner.get_OsCurrentUser()
	print("Current User:", name)

	# Tester for get_OsGroups() function
	groups = scanner.get_OsGroups() # Returns a struct of a group {gr_name, gr_passwd, gr_gid, gr_mem} 
									# Group Name, Group password, Numerical Group ID, Group Member's User names
	print("Current Groups:")
	for group in groups:
		print(group.gr_name + "\t" + str(group.gr_gid)) # Print each group name and group id