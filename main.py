# LEGAL
# https://legal.linkedin.com/api-terms-of-use

# Non-official sources I used:
# https://www.youtube.com/watch?v=kCggyi_7pHg
# https://www.jcchouinard.com/authenticate-to-linkedin-api-using-oauth2/

from fastapi import FastAPI
import facebook
import json
import requests
import random
import string

from dictionaries.Facebook_data import Facebook_data as fbd
from dictionaries.Instagram_data import Instagram_data as igd
from dictionaries.Linkedin_data import Linkedin_data as lnd
from dictionaries.Twitter_data import Twitter_data as twd

from authentication.ln_authentication import auth, headers


# If you go to index endpoint and add /docs, you get Swagger and it automatically generates the documentation
# Or you can go to index endpoint and add /redoc, which gives you another documentation for your API
# Error messages are also automatically generated

app = FastAPI() # Instantiate an app object. Now we can start writing the endpoints.

# Create a list of all static data for social media platforms.
data_ditionary = {
    'fb': fbd.dict,
    'ig': igd.dict,
    'ln': lnd.dict,
    'tw': twd.dict
}

ln_credentials = 'ln_credentials.json'

fb_token = ''
ig_token = ''
tw_token = ''


# When you query, the app checks if all permissions are avaliable and if not it asks you for the permission - aka prompts login and creates access token

'''
These are endpoints with "instructions", there is only text explaining what can you query for each social media
'''
@app.get('/') 
def home():
    return ('To so navodila, kako uporabljat api.')

@app.get('/facebook')
def facebook_home():
    return('fb placeholder')

@app.get('/instagram')
def instagram_home():
    return('ig placeholder')

@app.get('/twitter')
def twitter_home():
    return('tw placeholder')

@app.get('/linkedin')
def linkedin_home():
    return('ln placeholder')






###########################################
# Functions for calling social media apis #
###########################################

def call_facebook(endpoint, parameters, fb_token):
    if parameters == '':
        response = requests.get(f'https://graph.facebook.com/{endpoint}?&access_token={fb_token}')
    else:
        response = requests.get(f'https://graph.facebook.com/{endpoint}?{parameters}&access_token={fb_token}')
    return response.json()

def call_instagram(endpoint, parameters, ig_token):
    response = requests.get(f'https://graph.facebook.com/{endpoint}?{parameters}&access_token={ig_token}')
    return response.json()

def call_linkedin(endpoint, parameters, headers):
    if parameters == '':
        response = requests.get(f'https://api.linkedin.com/v2/{endpoint}', headers = headers)
    else:
        response = requests.get(f'https://api.linkedin.com/v2/{endpoint}?{parameters}', headers = headers)
    return response.json()

def call_twitter(endpoint, parameters, tw_token):
    response = requests.get(f'https://graph.facebook.com/{endpoint}?{parameters}&access_token={tw_token}')
    return response.json()



'''
Returns data about the user specified by parameter fields
'''
# FURTHER DEVELOPMENT: If no fields are provided, all possible fields will be returned (for now, default fields are returned)

@app.get('/me')
def get_data_about_user():
    requested_social_media = 'ln'.split(',') # TEST
    
    #  see which platforms need to be queried based on parameter 'social'
    requested_social_media_data = [] # contains data dictionaries of selected social media platforms
    for social_media in requested_social_media:
        requested_social_media_data.append(data_ditionary[social_media])


    fields = 'name,id'.split(',') # TEST TODO: get value of parameter fields somehow


    # map fields for similar parameter for each platform
    mapped_fields = [] # contains string of selected fields corresponding to platforms from selected_social_media
    for social_media in requested_social_media_data:
        temp_fields = ''
        for field in social_media['field_mapping']:
            temp_fields += social_media['field_mapping'][field] + ','
        mapped_fields.append(temp_fields[:-1])

    # perform calls to social media APIs
    if 'fb' in requested_social_media:
        fb_response = call_facebook('me', 'fields' + mapped_fields[requested_social_media.index('fb')], fb_token) # json response
        print(fb_response)
    
    if 'ig' in requested_social_media:
        ig_response = call_instagram('', '', ig_token)
    
    if 'ln' in requested_social_media:
        ln_access_token = auth(ln_credentials) # Authenticate the LinkedIn API
        ln_headers = headers(ln_access_token) # Prepare headers to attach to request
        ln_response = call_linkedin('me', 'fields' + mapped_fields[requested_social_media.index('ln')], ln_headers)
        print(ln_response)

    if 'tw' in requested_social_media:
        tw_response = call_twitter('', '', tw_token)

    # get value for each field
    # Aggregate responses into something like: 

    {'poenoteno_ime_prvega_podatka': [
        {
            'provider': 'Facebook',
            'nepoenoteno_ime_prvega_podatka': 'podatek'
        },
        {
            'provider': 'Instagram',
            'nepoenoteno_ime_prvega_podatka': 'podatek'
        }
    ],
    'poenoteno_ime_drugega_podatka': [{},{}]
    }

    # FURTHER DEVELOPMENT: If too much time, implement parameter "group_by" that allows you to either group by data first or by provider first.


# FB CALL EXAMPLES

# graph = facebook.GraphAPI(access_token=token, version = 3.1)
# # events = graph.request('/masa.smajila?metadata=1&access_token='+token)
# # print (events)

# page = graph.get_object("Recipes", fields='name,about')
# print (json.dumps(page))




get_data_about_user()