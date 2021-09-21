#!/usr/bin/env python
    
'''
This is modified code from
Simple Authentication script to log-on the Linkedin API by Jean-Christophe Chouinard. 
@website:   jcchouinard.com
'''
import json
import random
import requests
import string
from .utility import Utility as ut

'''
Run the Authentication.
If the access token exists, it will use it to skip browser auth.
If not, it will open the browser for you to authenticate.
You will have to manually paste the redirect URI in the prompt.
'''

def auth(file_with_credentials):

    creds = ut.read_credentials(file_with_credentials)
    client_id, client_secret = creds['client_id'], creds['client_secret']
    redirect_uri = creds['redirect_uri']
    api_url = 'https://www.linkedin.com/oauth/v2' 
        
    args = client_id, client_secret, redirect_uri
    authorize(api_url, *args) 


def auth_part_2(auth_code, file_with_credentials):

    creds = ut.read_credentials(file_with_credentials)
    client_id, client_secret = creds['client_id'], creds['client_secret']
    redirect_uri = creds['redirect_uri']
    args = client_id, client_secret, redirect_uri

    access_token = refresh_token(auth_code, *args)
    return access_token

def create_header(access_token):
    '''
    Make the headers to attach to the API call.
    '''
    headers = {
    'Authorization': f'Bearer {access_token}',
    'cache-control': 'no-cache',
    'X-Restli-Protocol-Version': '2.0.0'
    }
    return headers

def create_CSRF_token():
    '''
    This function generate a random string of letters.
    It is not required by the Linkedin API to use a CSRF token.
    However, it is recommended to protect against cross-site request forgery
    For more info on CSRF https://en.wikipedia.org/wiki/Cross-site_request_forgery
    '''
    letters = string.ascii_lowercase
    token = ''.join(random.choice(letters) for i in range(20))
    return token

def open_url(url):
    '''
    Function to Open URL.
    Used to open the authorization link
    '''
    import webbrowser
    webbrowser.open(url)

def authorize(api_url,client_id,client_secret,redirect_uri):
    # Request authentication URL
    csrf_token = create_CSRF_token()
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'state': csrf_token,
        'scope': 'r_liteprofile,r_emailaddress,w_member_social'
        }

    response = requests.get(f'{api_url}/authorization',params=params)
    open_url(response.url)

def refresh_token(auth_code,client_id,client_secret,redirect_uri):
    '''
    Exchange a Refresh Token for a New Access Token.
    '''
    access_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'

    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
        }

    response = requests.post(access_token_url, data=data, timeout=30)
    response = response.json()
    access_token = response['access_token']
    return access_token

if __name__ == '__main__':
    credentials = 'credentials.json'
    access_token = auth(credentials)