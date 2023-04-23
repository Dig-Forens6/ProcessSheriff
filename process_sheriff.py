import psutil   # Importing all required libraries
import hashlib
from time import sleep
import subprocess
import cryptocode
import argparse
from twilio.rest import Client


def signature_verify(binary_path, sig_check_type):
    """
    This is signature_verify function, it checks whether a binary file is singed
    Input: path for binary file
    Output: True or False
    """
    signature_check = subprocess.Popen(["sigcheck.exe", binary_path], stdout=subprocess.PIPE,
                                       creationflags=subprocess.CREATE_NO_WINDOW)  # Signature info from binary files
    capture_out, errors = signature_check.communicate()
    if sig_check_type == 'M':
        if b'Signed' and b'Microsoft Corporation' in capture_out:    # Checking the signature
            return True
        else:
            return False
    elif sig_check_type == 'A':
        if b'Signed' in capture_out:         # Checking the signature
            return True
        else:
            return False
    else:
        print('\nYou did not input a correct scan type!')
        exit()


def decrypt_path(encypted_path, password):
    """
    This is decrypt_path function, it decrypts the path for file containing whitelisted hashes
    Input: Encrypted file path and decryption password
    Output: Decrypted file path
    """
    try:
        decrypted_path = cryptocode.decrypt(encypted_path, password)    # Decrypting directory path for hash list
        return decrypted_path
    except TimeoutError:
        print('\nYou did not input a correct decryption password!')


def alert_messages(status):
    """
    This is the alert_messages function, it sends alert SMS message when a non-whitelisted binary was found
    Input: Process termination status
    Output: None
    """
    twilio_sid = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    twilio_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    twilio_client = Client(twilio_sid, twilio_token)   # Creating Twilio client to send SMS messages
    if status == 'Terminated':
        alert = "UNTRUSTED PROCESS WAS TERMINATED!"
    else:
        alert = "UNTRUSTED PROCESS COULD NOT BE TERMINATED!"
    twilio_client.messages.create(body=alert, from_='+1XXXXXXXXXX', to='+1XXXXXXXXXX')   # Sending SMS message
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process monitoring program.')
    parser.add_argument('--pass_word', '-p', help='Password to decrypt directory path for hash list')
    parser.add_argument('--scan_int', '-s', help='Number of seconds between scans')
    parser.add_argument('--allow_type', '-t', help="Allow only Microsoft 'M' or all 'A' signed binaries")
    args = parser.parse_args()
    password = args.pass_word
    scan_intervals = args.scan_int    # Number of iterations before full process scan
    sig_check_type = args.allow_type  # Type of signed binaries allowed to run ('M' for Microsoft or 'A' for all signed)
    print("\nProcessSheriff scanning all running processes..........")
    pid_list_reset = 1000     # Number of iterations before full process scan
    pid_list = []                  # List for running processes allowed to continue running
    encypted_path = r'75Gm7XPRJnxbArg1ZS6rdLuSuCljPpAizPEEHd6zF29JI7r8ippdBIm/Vl0qruEXEnNrCso=*A2ryoS9T0G7iVl' \
                    r'o2CeB4og==*UnPwkXBqAd4cx21DRWqd6Q==*/SRQzcsVeWuZYNDKUU46ag=='  # Encrypted path for hash list file
    path = decrypt_path(encypted_path, password)    # Calling function to decrypt the directory path for hash list
    read_file = open(path, 'r')
    known_hashes = read_file.read()
    while True:                         # Creating infinite loop for continuous scanning
        process_list = psutil.process_iter()   # List of running processes
        for proc in process_list:
            proc_pid = proc.pid   # Getting process ID's for running processes
            if proc_pid in pid_list:           # Preventing rescanning of already cleared running processes
                continue
            proc_name = proc.name()     # Getting process name
            try:
                binary_path = proc.exe()     # Getting binary path
            except:
                executable = False
                continue

            if binary_path is not False and '\\' in binary_path:
                try:
                    check_sig = signature_verify(binary_path, sig_check_type)    # Calling function to check signature
                except:
                    check_sig = False
                if check_sig is True:
                    pid_list.append(proc_pid)      # Adding cleared processes to the list
                    continue
                else:
                    try:
                        file_data = open(binary_path, 'rb').read()
                        my_md5 = hashlib.md5()
                        my_md5.update(file_data)            # Hashing binary if it is not signed
                        md5_value = my_md5.hexdigest()
                    except:
                        md5_value = 'NA'                  # Value assigned if hashing failed
            else:
                md5_value = 'NA'
            if md5_value in known_hashes or md5_value == 'NA':
                pid_list.append(proc_pid)                        # Adding cleared processes to the list
                continue
            else:
                try:
                    proc.terminate()                    # Terminating non-whitelisted processes
                    alert_messages('Terminated')            # Calling function to send alert SMS message
                    print('\n-----------------TERMINATED PROCESS----------------', '\nPID: ', proc_pid, '\nName: ',
                          proc_name, '\nExecutable: ', binary_path, '\nMD5: ', md5_value, '\nStatus: Terminated')

                except:
                    alert_messages('Not_Terminated')      # Calling function to send alert SMS message
                    print('\n-----------------UNTRUSTED PROCESS----------------', '\nPID: ', proc_pid, '\nName: ',
                          proc_name, '\nExecutable: ', binary_path, '\nMD5: ', md5_value,
                          '\nStatus: Active - Manual Termination Required')
        pid_list_reset -= 1
        if pid_list_reset == 0:        # Resetting process information to conduct full scan of running processes
            pid_list = []
            pid_list_reset = 1000
        sleep(int(scan_intervals))       # Pausing process scans for a number of seconds
