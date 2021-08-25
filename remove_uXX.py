#!/usr/bin/env python3
'''
this script removes versions of contacts that have uXXXXX@live.warwick.ac.uk email addresses
'''

import requests
import xml.etree.ElementTree as ET
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import hashlib
import os
from dotenv import load_dotenv
load_dotenv()

SU_ENDPOINT = os.getenv("SU_ENDPOINT")
MC_API_KEY = os.getenv("MC_API_KEY")
MC_SERVER = os.getenv("MC_SERVER")
MC_LIST_ID = os.getenv("MC_LIST_ID")

def setup_client():
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": MC_API_KEY,
        "server": MC_SERVER
    })
    return client


def main():

    client = setup_client()

    response = requests.get(SU_ENDPOINT)
    root = ET.fromstring(response.text)

    print(root)

    for child in root:
        fname = (child.find('FirstName').text).title()
        lname = (child.find('LastName').text).title()
        # email = child.find('EmailAddress').text
        email = "u" + child.find('UniqueID').text + "@live.warwick.ac.uk"
        subscriber_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()

        print("removing", fname, lname, email, "from mailchimp")

        try:
            response = client.lists.delete_list_member(MC_LIST_ID, subscriber_hash)
            print(response)
        except ApiClientError as error:
            print("Error: {}".format(error.text))


if __name__ == "__main__":
    main()
