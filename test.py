from main import *

'''
This script imports all the methods from `main.py` and tests them individually. 
'''

client = setup_client()
data = get_data()

email = "test@soneji.xyz"
subscriber_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
name = "Test"

add_to_mc(client, name, name, email, subscriber_hash)
