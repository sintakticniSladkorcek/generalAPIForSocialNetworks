import json
from facebook import GraphAPI
from .utility import Utility as ut

def auth(file_with_credentials):
    credentials = ut.read_credentials(file_with_credentials)
    app_token, user_token = credentials['fb_app_token'], credentials['fb_user_token']
    return user_token
 
# graph = GraphAPI(access_token = user_token)

# TODO: Improve with https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow/