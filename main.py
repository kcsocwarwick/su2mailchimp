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
        "server": MC_SERVER,
    })
    return client


def get_data():
    response = requests.get(SU_ENDPOINT)
    data = ET.fromstring(response.text)
    return data


def add_to_mc(client, fname, lname, email, subscriber_hash):
    response = client.lists.set_list_member(
        MC_LIST_ID,
        subscriber_hash, {
            "email_address": email,
            "status_if_new": "subscribed",
            "merge_fields": {
                "FNAME": fname,
                "LNAME": lname,
            }
        }
    )

    return response


def main():

    client = setup_client()
    data = get_data()

    for person in data:
        fname = (person.find('FirstName').text).title()
        lname = (person.find('LastName').text).title()
        email = person.find('EmailAddress').text
        subscriber_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()

        print("Adding", fname, lname, email, "to mailchimp")

        try:
            response = add_to_mc(client, fname, lname, email, subscriber_hash)
            print("Success:", response['id'], response['email_address'], "is", response['status'])
        except ApiClientError as error:
            print("Error: {}".format(error.text))


if __name__ == "__main__":
    main()
