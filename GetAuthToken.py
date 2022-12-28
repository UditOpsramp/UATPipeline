#! /usr/bin/python3

import requests
import json

token = ''


def GetAuthToken(clientkey, clientsecret, portal):

    global token

    url = "https://"\
          + portal +\
          "/auth/oauth/token"

    payload = {
        'grant_type': 'client_credentials',
        'client_id': clientkey,
        'client_secret': clientsecret
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    json = response.json()
    token = (json['access_token'])
