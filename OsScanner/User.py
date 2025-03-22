# Define a user class for having User objects that represent all the system users
class User:

	def __init__(self, username, hasPassword, uid,guid, homedir, shell):
		
		# The username can be filtered out of the /etc/passwd file for linux 
		self.username = str(username)
		
		if str(hasPassword) != "":
			self.hasPassword = True
		else:
			self.hasPassword = False
		
		self.userid = str(uid)
		
		self.groupid = str(guid)

		self.home_dir = str(homedir)
		
		self.shell = str(shell)