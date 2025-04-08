import subprocess



def split_and_run(script1, script2, session_name="split_session"):

	subprocess.run(["tmux", "new-session", "-d", "-s", "split_session", f"python3 {script2}; bash"])

	#subprocess.run(["tmux", "split-window", "-h", "-t", "split_session", f"python3 {script2}; bash"])

	#subprocess.run(["tmux", "select-layout", "-t", session_name, "even-horizontal"])

	#subprocess.run(["tmux", "attach-session", "-t", session_name])






if __name__ == "__main__":
	split_and_run("query_osv.py", "query_nvd.py")
	

