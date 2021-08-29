import tweepy
import webbrowser
from .utility import Utility as ut

def auth(file_with_credentials):
    creds = ut.read_credentials(file_with_credentials)
    consumer_key, consumer_secret_key, redirect_uri = creds['consumer_key'], creds['consumer_secret_key'], creds['redirect_uri']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key, redirect_uri)

    redirect_url = auth.get_authorization_url()
    webbrowser.open(redirect_url)

    user_pin_input = input('Please enter the PIN here: ')

    user_access_keys = auth.get_access_token(user_pin_input)
    creds.update({'user_access_token':auth.access_token})
    creds.update({'user_access_token_secret':auth.access_token_secret})
    ut.save_token(file_with_credentials, creds)

    return auth