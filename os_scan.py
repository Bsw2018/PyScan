"""
Scanner for gathering information from the operating system

"""

import os
import pwd
import grp
import stat
import subprocess
from User import User
import tkinter as tk
from tkinter import ttk
from Group import Group


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
			for user in pwd.getpwall():
				self.OsUsers.append(User(user.pw_name, user.pw_passwd, user.pw_uid, user.pw_gid, user.pw_dir, user.pw_shell))
		else:
			self.OsUsers = []

		return self.OsUsers


	def get_OsGroups(self):
		try:
			groups = grp.getgrall()
		except Excpetion:
			groups = []

		for group in groups:
			self.OsGroups.append(Group(group.gr_name, group.gr_passwd, group.gr_gid, group.gr_mem))

		return self.OsGroups
		

	def gatherFileSystem(self):
		pass

	def checkBadPermissions(self):
		pass


if __name__ == "__main__":
	scanner = OsScanner()
	
	# Tester for get_OsCurrentUser functions
	#name = scanner.get_OsCurrentUser()
	#print("Current User:", name)

	root = tk.Tk()
	root.title("User Table")
	root.geometry("800x1800")

	notebook = ttk.Notebook(root)
	notebook.pack(expand=True, fill="both")

	table_frame = ttk.Frame(notebook)
	notebook.add(table_frame, text="User Table")


	style = ttk.Style(table_frame)
	style.configure("Treeview",
					background="#F0F0F0",
					foreground="black",
					rowheight=25,
					fieldbackground="#F0F0F0")
	style.configure("Treeview.Heading",
					background="#4a4a4a",
					foreground="white",
					relief="flat")

	columns = ("username", "password", "uid", "gid", "home_dir", "shell")
	tree = ttk.Treeview(table_frame, columns=columns, show="headings")

	for col in columns:
		tree.heading(col, text=col.capitalize(), anchor="center")
		tree.column(col, anchor="center", width=100)

	tree.heading("username", text="Username")
	tree.heading("password", text="Password")
	tree.heading("uid", text="UID")
	tree.heading("gid", text="GID")
	tree.heading("home_dir", text="Home Directory")
	tree.heading("shell", text="Shell")

	tree.column("username", width=100)
	tree.column("uid", width=50)
	tree.column("gid", width=50)
	tree.column("home_dir", width=150)
	tree.column("shell", width=100)


	for index,user in enumerate(scanner.get_OsUsers()):
		
		tag = "evenrow" if index % 2 == 0 else "oddrow"

		tree.insert("","end" , values=(
			user.username, 
			user.hasPassword, 
			user.userid, 
			user.groupid, 
			user.home_dir, 
			user.shell), tags=(tag,))


	tree.tag_configure("evenrow", background="#E8E8E8")
	tree.tag_configure("oddrow", background="#DFDFDF")


	tree.pack(expand=True, fill="both")


	root.mainloop()


	#Tester for get_OsUsers:
	


	# Tester for get_OsGroups() function
	groups = scanner.get_OsGroups() # Returns a struct of a group {gr_name, gr_passwd, gr_gid, gr_mem} 
									# Group Name, Group password, Numerical Group ID, Group Member's User names
	print("Current Groups:")
	for group in scanner.get_OsGroups():
		print(group.name + str(group.hasPassword) + str(group.group_id), end="") # Print each group name and group id
		for member in enumerate(group.members):
			print(member)
		print()


