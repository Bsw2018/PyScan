# Class object for a Group

class Group:

	def __init__(self, groupname, hasPassword, group_id, group_members):
		self.name = groupname

		if hasPassword == "":
			self.hasPassword = False
		else:
			self.hasPassword = True

		self.group_id = group_id

		self.members = group_members