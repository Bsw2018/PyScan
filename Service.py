# The Service class definition file


import subprocess
import re


class Service:

	def __init__(self, name):
		self.serviceName = name # Service name
		self.serviceStatus = self.get_statusByName() # Service status: active, inactive, activating, deactivating, failed, None if can not be found
		self.pid = self.get_servicePID()
		

		self.serviceOwner = self.get_serviceOwner() # Service user owner
		self.serviceGroup = self.get_serviceGroup() # Service group owner
		#	self.servicePermissions = # Service permissions

	# This function gets the status of a service by using the systemctl status "service_name"
	def get_statusByName(self):

		try:
			# Capture the output strings from running the systemctl status command
			output = subprocess.check_output(['systemctl', 'status', self.serviceName], universal_newlines=True)

			if(output):
		
				#Split the output string by newline character
				lines = output.split('\n')
	
				# Iterate through the output lines
				for line in lines:
				
					# Try to find a match for the string proceeding the 'Active: ' string
					statusMatch = re.match(r'^\s*Active:\s+(\S+)', line)
					
					# If a match is found 
					if statusMatch is not None:
						return (statusMatch.group(1))
					else:
						continue

		except:
			return None
		
	# This function gets the process id from running the systemctl status command
	def get_servicePID(self):

		try:
			# Capture the output strings from the systemctl status command
						# Capture the output strings from running the systemctl status command
			output = subprocess.check_output(['systemctl', 'status', self.serviceName], universal_newlines=True)

			if(output):
		
				#Split the output string by newline character
				lines = output.split('\n')
	
				# Iterate through the output lines
				for line in lines:
				
					# Try to find a match for the string proceeding the 'Active: ' string
					pidMatch = re.match(r'^\s*Main PID:\s+(\S+)', line)
					
					# If a match is found 
					if pidMatch is not None:
						return (pidMatch.group(1))
					else:
						continue

				return "None" # Returns the string None if no process id is found 

		except:
			return str(None)

	def get_serviceOwner(self):
		
		if self.pid != "None":
			
			try:
				output = subprocess.check_output(["ps", "-o", "user=", "-p", self.pid], universal_newlines=True)

				if output:
					output = strip("\n")
					return output
			except:
				return "Unknown"

		else:

			return "None"

	def get_serviceGroup(self):

		if self.pid != "None":
			
			try:
				output = subprocess.check_output(["ps", "-o", "group=", "-p", self.pid], universal_newlines=True)

				if output:
					output = strip("\n")

					return output
			except:
				return "Unknown"

		else:

			return "None"