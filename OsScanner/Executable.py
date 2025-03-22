# Class definition for Operating System Executables
# The purpose of the class is to have an object representing all of the exectuables in the file system
# The objects will be created based off of executables found in the '/bin' folder and the '/usr/bin' folder
# The Executable object will have a few attributes:
	# Name : str 
	# Path : str
	# Owner : str
	# Group : str
	# Permissions : str



import os
import pwd
import grp
import stat
from pathlib import Path

class Executable:

	# The executable objects are initialized based off the output of a listdir python function called in the OsScanner's get_OsExecutables method
	def __init__(self, name, path):

		self.Name = name

		self.Path = path + name

		self.Owner = self.get_Owner()

		self.Group = self.get_Group()

		self.Permissions = self.get_Permissions()

	def get_Owner(self):

		file_stat = os.stat(self.Path)
		uid = file_stat.st_uid

		return str(pwd.getpwuid(uid).pw_name)

	def get_Group(self):

		file_stat = os.stat(self.Path)
		gid = file_stat.st_gid

		return str(grp.getgrgid(gid).gr_name)

	def get_Permissions(self):

		return(stat.filemode(Path(self.Path).stat().st_mode))