import json
from requests_oauthlib import OAuth1Session

def auth_on_bricklink():
    with open('auth_credentials.json', 'r') as json_data:
        auth_data = json.load(json_data)
        client = OAuth1Session(client_key=auth_data["client_key"],
                        client_secret=auth_data["client_secret"],
                        resource_owner_key=auth_data["resource_owner_key"],
                        resource_owner_secret=auth_data["resource_owner_secret"])
        return client