import json
from .utility import Utility as ut
import requests
import webbrowser


def auth(file_with_credentials):
    credentials = ut.read_credentials(file_with_credentials)
    client_id, redirect_uri = credentials['client_id'], credentials['redirect_uri']

    api_url = 'https://www.instagram.com/oauth/authorize'
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': 'user_profile,user_media'
    }

    response = requests.get(f'{api_url}',params=params)
    webbrowser.open(response.url)
    
def auth_part_2(code, file_with_credentials):
    credentials = ut.read_credentials(file_with_credentials)
    client_id, client_secret, redirect_uri = credentials['client_id'], credentials['client_secret'], credentials['redirect_uri']

    api_url = 'https://www.instagram.com/oauth/access_token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'code': code
    }

    response = requests.post(f'{api_url}',data=data)

    return response