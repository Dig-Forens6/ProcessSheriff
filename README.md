# Project Name: 
ProcessSheriff, dfor740_final_process_sheriff_args.py

# dfor740_final_process_sheriff_args.py : 
This Python program scans running processes in Microsoft Windows environment for unsigned or non-whitelisted binaries.

# Description: This program has the following functionalities
	- Scanning all running processes using psutil library. 
	- Determining binary path for each running process.
	- Checking whether a binary file was signed by Microsoft.
	- If binary file is not signed, it would be hashed and compared to whitelisted binaries. 
	- Terminating any process that has an unsigned binary file or part of the whitelisted binaries.
	- Sending alerts when a process has an unsigned binary or did not match whitelisted binaries.

# Requirements: 
	- The script requires Twilio SID and Token to be added to the code. 
	- Telephone numbers to be used as source and destination for the alert messages. 
	- A file containing a list of hashes of whitelisted binaries. 
	- Third-party libraries to be installed. 
	- Sigcheck – Sysinternals must be added in the same directory as the script file. 
	
# Required Libraries: 
	- psutil  
	- hashlib
	- time 
	- subprocess
	- cryptocode
	- getpass
	- twilio
	- argparse
	
# Command Switches: 
	'-p' switch is used to provide decryption password for the directory path of the hash list.
	'-s' switch is used to provide number of seconds between scans intervals. 
	'-t' switch is used to provide the scan mode, 'M' option only allows processes with Microsoft signed binaries and 'A' option allows processes with any signed binaries.
	
# Usage: Following are command examples
	- Command to show help menu: py dfor740_final_process_sheriff_args -h 
	- Command to only allow processes with Microsoft Signed Binaries: py dfor740_final_process_sheriff_args -p 123456 -s 3 -t M
	- Command to run the program as background process and allow processes with all signed binaries: pythonw dfor740_final_process_sheriff_args -p 123456 -s 3 -t A

# Obtaining Hash Lists:
	- The hash list can be built by hashing a clean system and adding any binaries that would be normally running in the system. 
	- There are free and pre-built hash lists provided by the National Institute of Standards and Technology (NIST), https://www.nist.gov/itl/ssd/software-quality-group/national-software-reference-library-nsrl/nsrl-download/current-rds.
	- There are commercials solutions that provide hash lists to be used for applications similar to this program, https://www.hashsets.com/.

# NOTE: 
The uploaded copy of the Python script is missing Twilio SID, Twilio Token, and phone numbers. Please add that informaiton before utlizing the sript. 
