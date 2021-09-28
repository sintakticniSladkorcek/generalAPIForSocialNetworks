import tweepy
from requests import Response
from requests_oauthlib import OAuth1Session
from authentication.utility import Utility as ut
import json

def me(api):
    return api.me()

function_mappings = {
    'me': me
}

def call_api(access_credentials, data_dictionary, method, endpoint, path, mapped_fields, id):
    print(mapped_fields)

    print('Composing oauth session')
    oauth = OAuth1Session(
    access_credentials.consumer_key,
    client_secret=access_credentials.consumer_secret,
    resource_owner_key=access_credentials.access_token,
    resource_owner_secret=access_credentials.access_token_secret,
    )

    headers = {
        'Authorization': f'Bearer {access_credentials.access_token}'
    }

    specific_endpoint = data_dictionary['endpoint_mapping'][endpoint]['endpoint']

    url = data_dictionary['base_url'] + specific_endpoint
    params = {}

    if specific_endpoint == 'me':
        api = tweepy.API(access_credentials)
        try:
            user = api.me()
            response = Response()
            response._content = bytes(json.dumps(user._json), 'utf-8')
            response.status_code = 200
            return response
        except Exception as e:
            response = Response()
            response.status_code = e.status_code
            response.reason = e.detail
            response.json = e.detail


    if id != None:
        url += f'?ids={id}'
    if path != None:
        specific_path = data_dictionary['endpoint_mapping'][endpoint]['paths'][path]['path']
        url += '/' + specific_path

    if method == 'get':
        # remove possible duplicates
        mapped_fields = list(dict.fromkeys(mapped_fields))

        # concatenate parameters into string
        temp = ''
        for field in mapped_fields:
            temp += field + ','
        
        if specific_endpoint == 'users':
            user_fields = temp[:-1]
            fields = f'user.fields={user_fields}'
        elif specific_endpoint == 'tweets':
            tweet_fields = temp[:-1]
            fields = f'tweet.fields={tweet_fields}'

        url = f'{url}&{fields}'

        # response = oauth.get(f'{url}', params=params)
        response = oauth.get(f'{url}')

        'https://api.twitter.com/2/users?ids=796807413319999488&user.fields=id,name,username'

    elif method == 'post':
        # call API
        response = requests.post(f'{url}', json=mapped_fields, headers=headers)

    return response