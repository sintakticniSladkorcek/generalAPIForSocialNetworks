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

from authentication.ln_authentication import headers
from authentication.ln_authentication import auth as ln_auth
from authentication.fb_authentication import auth as fb_auth


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

file_with_fb_credentials = 'fb_credentials.json'
file_with_ln_credentials = 'ln_credentials.json'
file_with_tw_credentials = 'tw_credentials.json'

fb_access_token = fb_auth(file_with_fb_credentials) # Authenticate FB API
ln_access_token = ln_auth(file_with_ln_credentials) # Authenticate the LinkedIn API



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




def map_fields(requested_social_media, fields):
    #  see which platforms need to be queried based on parameter 'social'
    requested_social_media_data = [] # contains data dictionaries of selected social media platforms
    for social_media in requested_social_media:
        requested_social_media_data.append(data_ditionary[social_media])

    # map fields for similar parameter for each platform
    mapped_fields = [] # contains string of selected fields corresponding to platforms from selected_social_media
    unified_fields = []
    for social_media in requested_social_media_data:
        temp_fields = ''

        if fields == []: # If no fields are selected, return all possible data
            for field in social_media['field_mapping']:
                temp_fields += social_media['field_mapping'][field] + ','
                unified_fields.append(social_media['field_mapping'].keys())
        else:
            for field in fields:
                temp_fields += social_media['field_mapping'][field] + ','
            unified_fields = fields
        
        mapped_fields.append(temp_fields[:-1])

    return unified_fields, mapped_fields


def merge_responses(fields, responses):
    merged_response = {}
    for field in fields:
        merged_response[field] = []
        for platform in responses:
            temp_dict = {}
            temp_dict['provider'] = data_ditionary[platform]['name']
            specific_field_name = data_ditionary[platform]['field_mapping'][field]
            # TODO: handle error responses
            temp_dict[specific_field_name] = responses[platform][specific_field_name] # error if we got error response from a platform
            merged_response[field].append(temp_dict)

    response = json.dumps(merged_response, indent=2)
    return response


###########################################
# Functions for calling social media apis #
###########################################

def call_social_media_APIs(requested_social_media, endpoint, mapped_fields, unified_fields):

    responses = {}

    if 'fb' in requested_social_media:
        fb_response = call_facebook(data_ditionary['fb']['endpoint_mapping'][endpoint], 'fields=' + mapped_fields[requested_social_media.index('fb')], fb_access_token) # json response
        responses['fb'] = fb_response
        print(json.dumps(fb_response, indent=2))
    
    if 'ig' in requested_social_media:
        ig_response = call_instagram(data_ditionary['ig']['endpoint_mapping'][endpoint], '', ig_token)
        responses['ig'] = ig_response
    
    if 'ln' in requested_social_media:
        ln_headers = headers(ln_access_token) # Prepare headers to attach to request
        ln_response = call_linkedin(data_ditionary['ln']['endpoint_mapping'][endpoint], 'fields=' + mapped_fields[requested_social_media.index('ln')], ln_headers)
        responses['ln'] = ln_response
        print(json.dumps(ln_response, indent=2))

    if 'tw' in requested_social_media:
        tw_response = call_twitter(data_ditionary['tw']['endpoint_mapping'][endpoint], '', tw_token)
        responses['tw'] = tw_response

    # merge responses into one json object
    response = merge_responses(unified_fields, responses)
    return response

def call_social_media_APIs_with_given_id(requested_social_media, endpoint, id, mapped_fields, unified_fields):
    responses = {}

    if 'fb' in requested_social_media:
        fb_response = call_facebook(data_ditionary['fb']['endpoint_mapping'][endpoint] + id, 'fields=' + mapped_fields[requested_social_media.index('fb')], fb_access_token) # json response
        responses['fb'] = fb_response
        print(json.dumps(fb_response, indent=2))
    
    if 'ig' in requested_social_media:
        ig_response = call_instagram(data_ditionary['ig']['endpoint_mapping'][endpoint] + id, '', ig_token)
        responses['ig'] = ig_response
    
    if 'ln' in requested_social_media:
        ln_headers = headers(ln_access_token) # Prepare headers to attach to request
        ln_response = call_linkedin(data_ditionary['ln']['endpoint_mapping'][endpoint] + id, 'fields=' + mapped_fields[requested_social_media.index('ln')], ln_headers)
        responses['ln'] = ln_response
        print(json.dumps(ln_response, indent=2))

    if 'tw' in requested_social_media:
        tw_response = call_twitter(data_ditionary['tw']['endpoint_mapping'][endpoint] + id, '', tw_token)
        responses['tw'] = tw_response

    # merge responses into one json object
    response = merge_responses(unified_fields, responses)
    return response

def call_facebook(endpoint, parameters, fb_token):
    if parameters == '':
        response = requests.get(f'https://graph.facebook.com/v11.0/{endpoint}?&access_token={fb_token}')
    else:
        response = requests.get(f'https://graph.facebook.com/v11.0/{endpoint}?{parameters}&access_token={fb_token}')
    return response.json()

    # Nested call https://graph.facebook.com/10215963448399509?fields=albums.limit(2){photos.limit(3)}
    # https://graph.facebook.com/NODE?fields=FIRSTLEVEL{SECOND LEVEL} can have even more levels
    # .limit limits the number of returned results

    # graph.facebook.com/me?fields=posts.limit(5){message,privacy{value}}
    # graph.facebook.com/me?fields=albums.limit(5){name,privacy,photos.limit(2){picture}},posts.limit(5){message, privacy}
    

def call_instagram(endpoint, parameters, ig_token):
    response = requests.get(f'https://graph.facebook.com/v11.0/{endpoint}?{parameters}&access_token={ig_token}')
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


########################
# Endpoint definitions #
########################

'''
Returns data about the user specified by parameter fields
'''

@app.get('/me')
def get_data_about_me(sm: str = 'fb,ln,tw', fields: str = ''):
    
    endpoint = 'me'
    requested_social_media = sm.split(',')
    fields = fields.split(',')

    # map fields
    unified_fields, mapped_fields = map_fields(requested_social_media, fields)

    # perform calls to social media APIs
    response = call_social_media_APIs(requested_social_media, endpoint, mapped_fields, unified_fields)
    return response



@app.get('/user/{user_id}')
def get_data_about_user(user_id: str, sm: str = 'fb,ln,tw', fields: str = ''):

    endpoint = 'user/'
    requested_social_media = sm.split(',')
    fields = fields.split(',')

    # map fields
    unified_fields, mapped_fields = map_fields(requested_social_media, fields)

    # perform calls to social media APIs
    response = call_social_media_APIs_with_given_id(requested_social_media, endpoint, user_id, mapped_fields, unified_fields)
    return response




# TODO: twitter authentication
# TODO: error handling
# TODO: ln authentication
# TODO: fb authentication
# TODO: check if already authenticated
    
    # FURTHER DEVELOPMENT: If too much time, implement parameter "group_by" that allows you to either group by data first or by provider first.
    # FURTHER DEVELOPMENT: When you query, the app checks if all permissions are avaliable and if not it asks you for the permission - aka prompts login and creates access token


# FB CALL EXAMPLES

# graph = facebook.GraphAPI(access_token=token, version = 3.1)
# # events = graph.request('/masa.smajila?metadata=1&access_token='+token)
# # print (events)

# page = graph.get_object("Recipes", fields='name,about')
# print (json.dumps(page))




# print(get_data_about_me(sm='fb,ln',fields='id,first_name,last_name'))
print(get_data_about_user('10215963448399509', 'fb', 'name,id,birthday'))