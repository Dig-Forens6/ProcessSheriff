# Project Name: 
ProcessSheriff

# process_sheriff.py : 
This Python program scans running processes in Microsoft Windows environment searching for unsigned or non-whitelisted binaries.

# Description: This program has the following functionalities
	- Scanning all running processes using psutil library. 
	- Determining binary path for each running process.
	- Checking whether a binary file was signed by Microsoft or other entities.
	- If a binary file is not signed, the binary hash would be compared to the whitelisted binaries. 
	- Terminating processes that have unsigned binaries or the binary hashes did not match the whitelisted binaries.
	- Sending alerts when a process has an unsigned binary or did not match the whitelisted binaries.

# Requirements: 
	- This program must be executed in an Administrator command prompt
	- The script requires Twilio SID and Token to be added to the code. 
	- Telephone numbers to be used as source and destination for the alert SMS messages. 
	- A file containing a list of hashes of whitelisted binaries. 
	- All third-party libraries to be installed. 
	- Sigcheck – Sysinternals must be added in the same directory as the script file, https://learn.microsoft.com/en-us/sysinternals/downloads/sigcheck 
	
# Required Libraries: 
	- psutil  
	- hashlib
	- time 
	- subprocess
	- cryptocode
	- twilio
	- argparse
	
# Command Switches: 
	'-p' switch is used to input the decryption password for the directory path of the hash list.
	'-s' switch is used to input the number of seconds between scans. 
	'-t' switch is used to provide the scan mode, 'M' option only allows processes with Microsoft signed binaries and 'A' option allows processes with all signed binaries.
	
# Usage: Following are command examples
	- Command to show help menu: py dfor740_final_process_sheriff_args.py -h 
	- Command to only allow processes with Microsoft signed binaries: py dfor740_final_process_sheriff_args.py -p 123456 -s 3 -t M
	- Command to allow processes with all signed binaries: py dfor740_final_process_sheriff_args.py -p 123456 -s 3 -t A
	- Command to run the program as background process: pythonw dfor740_final_process_sheriff_args.py -p 123456 -s 3 -t A

# Obtaining Hash Lists:
	- The hash list can be built by hashing a clean system and adding any binaries that would be normally running in that system. 
	- There are free and pre-built hash lists provided by the National Institute of Standards and Technology (NIST), https://www.nist.gov/itl/ssd/software-quality-group/national-software-reference-library-nsrl/nsrl-download/current-rds.
	- There are commercials solutions that provide hash lists to be used for applications similar to this program, https://www.hashsets.com/.

# NOTE: 
The copy of the Python script uploaded to GitHub is missing Twilio SID, Twilio Token, and phone numbers. Please add that informaiton before utlizing the provided sript. 
