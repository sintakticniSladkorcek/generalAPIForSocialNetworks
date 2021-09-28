import tweepy
import webbrowser
import json
from requests import Response
from .utility import Utility as ut

# This source helped: https://www.youtube.com/watch?v=dvAurfBB6Jk (29. 8.)

def auth(file_with_credentials):

    creds = ut.read_credentials(file_with_credentials)
    consumer_key, consumer_secret_key, redirect_uri = creds['consumer_key'], creds['consumer_secret_key'], creds['redirect_uri']

    try:

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key, redirect_uri)
        redirect_url = auth.get_authorization_url()
        webbrowser.open(redirect_url)

        user_pin_input = input('Please enter the PIN provided by Twitter here: ').strip()

        user_access_keys = auth.get_access_token(user_pin_input)
        return auth, None
    
    except Exception as e:
        response = Response()
        response.status_code = 400
        message = 'Something went wrong during the process of authenticating with Twiter. ' + str(e)
        error = {
                    'Error': {
                        'HTTPstatus': 400,
                        'error_code': 4,
                        'message': message
                    }
                }
        response.json = json.loads(json.dumps(error))
        return None, response
    