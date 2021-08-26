from main import *

'''
This script imports all the methods from `main.py` and tests them individually. 
'''

client = setup_client()
data = get_data()

email = "test2@soneji.xyz"
subscriber_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
name = "Test"

try:
    response = add_to_mc(client, name, name, email, subscriber_hash)
    print("Success:", response['id'], response['email_address'], "is", response['status'])
except ApiClientError as error:
    print("Error: {}".format(error.text))
    raise "rethrowing the error again lol"
