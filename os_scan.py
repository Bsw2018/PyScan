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
		self.OsCurrentUser = "" # Current user of the system

	# Get Current User function
	def get_OsCurrentUser(self):
		try:
			current_user = os.getlogin() # Returns a string denoting the name of the current user
		except Excpetion:
			current_user = pwd.getpwuuid(os.getuid()).pw_name # If exception, try to get user name through password database

		return current_user


	def set_OsCurrentUser(seelf)	

	# Get OsUsers List fuction
	def get_OsUsers(self):
		
		if self.OsType == 'posix':
			self.OsUsers = [user.pw_name for user in pwd.getpwall()]
		else:
			self.OsUsers = []

		return self.OsUsers


	def gatherGroupInfo(self):
		pass

	def gatherFileSystem(self):
		pass

	def checkBadPermissions(self):
		pass


if __name__ == "__main__":
	scanner = OsScanner()
	user_info = scanner.get_OsCurrentUser()
	print("Current User:", user_info)

	users = scanner.get_OsUsers()
	print("Current User List:")
	for user in users:
		print("\t\t  " + user)