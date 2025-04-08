"""
Scanner for gathering information from the operating system

"""

import os
import pwd
import grp
import stat
import re
import subprocess
import tkinter as tk
from tkinter import ttk
import urllib.parse
import json

from Group import Group
from User import User
from Service import Service
from Executable import Executable


class OsScanner:

    def __init__(self, output_file="system_info.json"):

        self.output_file = output_file

        self.OsType = os.name # Operating System Type 
        self.OsUsers = [] # List of system users
        self.OsGroups = [] # List of system groups
        self.OsServices = [] # List of system services
        self.OsCurrentUser = ""# Current user of the system
        self.OsExecutables = []

    # Get Current User method
    def get_OsCurrentUser(self):
        try:
            current_user = os.getlogin() # Returns a string denoting the name of the current user
        except Excpetion:
            current_user = pwd.getpwuuid(os.getuid()).pw_name # If exception, try to get user name through password database

        return current_user

    # Set OsCurrent method
    def set_OsCurrentUser(self):
        self.OsCurrentUser = self.get_OsCurrentUser()

    # Get OsUsers List method
    def get_OsUsers(self):
        
        if self.OsType == 'posix':
            for user in pwd.getpwall():
                self.OsUsers.append(User(user.pw_name, user.pw_passwd, user.pw_uid, user.pw_gid, user.pw_dir, user.pw_shell))
        else:
            self.OsUsers = []

        return self.OsUsers

    # Get OsGroups List method
    def get_OsGroups(self):
        try:
            groups = grp.getgrall()
        except Excpetion:
            groups = []

        for group in groups:
            self.OsGroups.append(Group(group.gr_name, group.gr_passwd, group.gr_gid, group.gr_mem))

        return self.OsGroups
        
    # Get OsServices List method
    def get_OsServices(self):
        
        # Find a way to get the running services on operating system

        # Method one: Use systemctl with the options list-units and --type=service

        try:
            output = subprocess.check_output(['systemctl','list-units','--type=service'], universal_newlines=True)
            
            lines = output.split('\n')

            for line in lines:
                
                nameMatch = re.match(r'^\s*(\S+)\.service', line)

                if nameMatch:
                    self.OsServices.append(Service(nameMatch.group(1)))
                else:
                    continue
        except:
            return "Error in running the systemctl command"

        return self.OsServices

    # Get OsExecutables List method
    def get_OsExecutables(self):
        
        # Check the files inside of the /bin folder and /usr/bin folder

        rootBinPath = "/bin/"

        binFiles = os.listdir(rootBinPath)

        for fileName in binFiles:

            self.OsExecutables.append(Executable(fileName, rootBinPath))

        return self.OsExecutables

    # Method for checking the sudoers file 
    def check_Sudoers(self):

        # Check and see if the '/etc/sudoers file has misconfigured permissions'
        sudoersPath = "/etc/sudoers"

        sudoersPerms = oct(os.stat(sudoersPath).st_mode)[-3:]

        return sudoersPerms

    # Method for gathering installed package information
    def get_installed_packages(self):

        installed_packages = []

        try:
        
            dpkg_output = subprocess.check_output(['dpkg-query', '-W', '-f=${Package} ${Version}\n'], encoding='utf-8')

            for line in dpkg_output.strip().split("\n"):
                package_name, package_version = line.split(' ', 1)
                clean_version = normalize_version(package_version)

                # Set vendor heuristically (adjust logic as needed)
                known_vendors = {
                    "openssl": "openssl",
                    "nginx": "f5",
                    "apache2": "apache",
                    "mysql-server": "oracle",
                    "python3": "python",
                }

                vendor = known_vendors.get(package_name, "debian")  # default to "debian"

                # Full CPE 2.3 format (13 fields)
                raw_cpe = f"cpe:2.3:a:{vendor}:{package_name}:{clean_version}:*:*:*:*:*:*:*"

                # URI-encode for later use in NVD API
                encoded_cpe = urllib.parse.quote(raw_cpe)

                installed_packages.append({
                    "name": package_name,
                    "version": package_version,
                    "normalized_version": clean_version,
                    "cpe": raw_cpe,
                    "encoded_cpe": encoded_cpe
                })
        
        except subprocess.CalledProcessError as e:
            print(f"Error gathering packages: {e}")


        software_data = {"installed_software": installed_packages}

        with open(self.output_file, 'w') as f:
            json.dump(software_data,f,indent=2)



def normalize_version(version):
    # Remove Debian/Ubuntu revision (e.g., "1.0.2ubuntu3" → "1.0.2")
    match = re.match(r"([\d\.]+)", version)
    return match.group(1) if match else version

if __name__ == "__main__":
    
    scanner = OsScanner()

    scanner.get_installed_packages()


    
    #Tester for check_Sudeors method

    # if scanner.check_Sudoers() in ['777', '666', '644', '600']:
    #   print("Potential Misconfiguration of Permissions for the sudoers file")
    # else:
    #   print("Sudoers File Check found no Misconfiguration")




    #Tester for the get_OsExecutables function

    # for executable in scanner.get_OsExecutables():
    #   print(executable.Name
    #            + "\t" + executable.Path
    #            + "\t" + executable.Owner
    #            + "\t" + executable.Group
    #            + "\t" + executable.Permissions)




    #Tester for the get_OsServices function
    # for service in scanner.get_OsServices():
    #   #if service.serviceName is not None:
    #   print(service.serviceName + ":")
    #   print("\t\t\t" + service.serviceStatus)
    #   print("\t\t\t" + service.pid)
    #   print("\t\t\t" + service.serviceOwner)
    #   print("\t\t\t" + service.serviceGroup)

    #   print("\n\n")

    # Tester for get_OsCurrentUser functions
    #name = scanner.get_OsCurrentUser()
    #print("Current User:", name)

    # root = tk.Tk()
    # root.title("User Table")
    # root.geometry("800x1800")

    # notebook = ttk.Notebook(root)
    # notebook.pack(expand=True, fill="both")

    # table_frame = ttk.Frame(notebook)
    # notebook.add(table_frame, text="User Table")


    # style = ttk.Style(table_frame)
    # style.configure("Treeview",
    #               background="#F0F0F0",
    #               foreground="black",
    #               rowheight=25,
    #               fieldbackground="#F0F0F0")
    # style.configure("Treeview.Heading",
    #               background="#4a4a4a",
    #               foreground="white",
    #               relief="flat")

    # columns = ("username", "password", "uid", "gid", "home_dir", "shell")
    # tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    # for col in columns:
    #   tree.heading(col, text=col.capitalize(), anchor="center")
    #   tree.column(col, anchor="center", width=100)

    # tree.heading("username", text="Username")
    # tree.heading("password", text="Password")
    # tree.heading("uid", text="UID")
    # tree.heading("gid", text="GID")
    # tree.heading("home_dir", text="Home Directory")
    # tree.heading("shell", text="Shell")

    # tree.column("username", width=100)
    # tree.column("uid", width=50)
    # tree.column("gid", width=50)
    # tree.column("home_dir", width=150)
    # tree.column("shell", width=100)


    # for index,user in enumerate(scanner.get_OsUsers()):
        
    #   tag = "evenrow" if index % 2 == 0 else "oddrow"

    #   tree.insert("","end" , values=(
    #       user.username, 
    #       user.hasPassword, 
    #       user.userid, 
    #       user.groupid, 
    #       user.home_dir, 
    #       user.shell), tags=(tag,))


    # tree.tag_configure("evenrow", background="#E8E8E8")
    # tree.tag_configure("oddrow", background="#DFDFDF")


    # tree.pack(expand=True, fill="both")


    # root.mainloop()


    #Tester for get_OsUsers:
    


    # Tester for get_OsGroups() function
    # groups = scanner.get_OsGroups() # Returns a struct of a group {gr_name, gr_passwd, gr_gid, gr_mem} 
    #                               # Group Name, Group password, Numerical Group ID, Group Member's User names
    # print("Current Groups:")
    # for group in scanner.get_OsGroups():
    #   print(group.name + str(group.hasPassword) + str(group.group_id), end="") # Print each group name and group id
    #   for member in enumerate(group.members):
    #       print(member)
    #   print()


