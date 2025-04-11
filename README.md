# PyScan
A python vulnerability scanner for detecting CVEs.<br><br> 

## Prerequisites

`tkinter` must be installed and is not available through pip.  
Install using your operating system's package manager:<br>

	  "Ubuntu/Debian: sudo apt install python3-tk\n"
	  "Fedora: sudo dnf install python3-tkinter\n"
      "Arch: sudo pacman -S tk\n"
      "Windows: Reinstall Python with tkinter\n"
      "macOS (Homebrew): brew install python-tk"<br><br> 

Querying the NIST NVD does not require an api token.<br>
However, **query_nvd.py** utilizes an api token and therefore it is recommended to visit the NIST website and have one automatically generated for you. <br>
They are free, instant, and allow faster queries.