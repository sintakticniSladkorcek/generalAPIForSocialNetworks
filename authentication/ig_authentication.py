import json
from facebook import GraphAPI
from .utility import Utility as ut
import requests

def auth(file_with_credentials):
    credentials = ut.read_credentials(file_with_credentials)
    client_id, redirect_uri = credentials['client_id'], credentials['redirect_uri']

    # https://www.instagram.com/accounts/login/?force_authentication=1&enable_fb_login=1&next=/oauth/authorize%3Fclient_id%3D216293130482337%26redirect_uri%3Dhttps%3A//127.0.0.1%3A443/ig_auth%26scope%3Duser_profile%2Cuser_media%26response_type%3Dcode
    # api_url = 'https://www.instagram.com/accounts/login/'
    # params = {
    #     'force_authentication': 1,
    #     'enable_fb_login': 1,
    #     'next': f'/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=user_profile,user_media&response_type=code'
    # }
    
    
    # https://www.instagram.com/oauth/authorize?client_id=216293130482337&redirect_uri=https://127.0.0.1:443/ig_auth&scope=user_profile%2Cuser_media&response_type=code
    api_url = 'https://www.instagram.com/oauth/authorize'
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': 'user_profile,user_media'
    }
    print(params)

    response = requests.get(f'{api_url}',params=params)
    print(response)
    return response

def auth_part_2(code, file_with_credentials):

    credentials = ut.read_credentials(file_with_credentials)
    client_id, client_secret, redirect_uri = credentials['client_id'], credentials['client_secret'], credentials['redirect_uri']

    api_url = 'https://api.instagram.com/oauth/access_token'
    params = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    response = requests.post(f'{api_url}',params=params)

    import webbrowser
    print(response.url)
    webbrowser.open(response.url)

    print(response.json())
    return response