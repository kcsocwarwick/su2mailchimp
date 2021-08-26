from main import *

'''
This script imports all the methods from `main.py` and tests them individually. 
'''

print("Setting up client...")
client = setup_client()
print("Client setup successfully")

print("Getting data...")
data = get_data()
print("Data retrieved successfully")


print("Adding test user to subscriber base...")

email = "test2@soneji.xyz"
subscriber_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
name = "Test"

try:
    response = add_to_mc(client, name, name, email, subscriber_hash)
    print("Success:", response['id'], response['email_address'], "is", response['status'])
except ApiClientError as error:
    print("Error: {}".format(error.text))
    raise "rethrowing the error again lol"

print("User added successfully")
