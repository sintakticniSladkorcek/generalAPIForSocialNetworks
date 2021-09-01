# LEGAL
# Facebook: https://developers.facebook.com/devpolicy/
#           https://developers.facebook.com/terms/dfc_platform_terms/
#           https://www.facebook.com/policies_center
# LinkedIn: https://legal.linkedin.com/api-terms-of-use
#           https://www.linkedin.com/legal/user-agreement
# Twitter:  https://developer.twitter.com/en/developer-terms
#           https://twitter.com/en/tos

# OFFICIAL SOCIAL MEDIA APIs DOCUMENTATION
# Facebook: https://developers.facebook.com/docs/graph-api/reference
# LinkedIn: https://docs.microsoft.com/en-us/linkedin/
# Twitter: https://developer.twitter.com/en/docs

# Non-official sources that helped in writing this code:
# https://www.youtube.com/watch?v=kCggyi_7pHg
# https://www.jcchouinard.com/authenticate-to-linkedin-api-using-oauth2/

from fastapi import FastAPI, HTTPException
import facebook # TODO: Do we need this library?
import tweepy # TODO: Do we need this library?
import json
import requests
import random
import string

from dictionaries.Facebook_data import Facebook_data as fbd
from dictionaries.Instagram_data import Instagram_data as igd
from dictionaries.Linkedin_data import Linkedin_data as lnd
from dictionaries.Twitter_data import Twitter_data as twd

from authentication.ln_authentication import create_header as create_ln_header
from authentication.ln_authentication import auth as ln_auth
from authentication.fb_authentication import auth as fb_auth
from authentication.tw_authentication import auth as tw_auth


# If you go to index endpoint and add /docs, you get Swagger and it automatically generates the documentation
# Or you can go to index endpoint and add /redoc, which gives you another documentation for your API
# Error messages are also automatically generated

app = FastAPI() # Instantiate an app object.

# Create a list of all static data and mappings for social media platforms.
data_dictionary = {
    'fb': fbd.dict,
    'ig': igd.dict,
    'ln': lnd.dict,
    'tw': twd.dict
}

# Specify documents with credentials
file_with_fb_credentials = 'fb_credentials.json'
file_with_ln_credentials = 'ln_credentials.json'
file_with_tw_credentials = 'tw_credentials.json'

# Authenticate
fb_access = fb_auth(file_with_fb_credentials)

ln_access = ln_auth(file_with_ln_credentials)

tw_creds, tw_error = tw_auth(file_with_tw_credentials)
if tw_error != None:
    tw_access = tw_creds
    print(tw_error, tw_error.json)
    # TODO: raise Exception or somehow include tw_error in a merged response

tw_access = tw_creds

# fb_api = facebook.GraphAPI(access_token=fb_access, version = 3.1)
# tw_api = tweepy.API(tw_access)
# me = tw_api.me()
# print(me._json) # returns json
# timeline = tw_api.user_timeline(user_id=me.id, count=200)
# print(timeline)


'''
These are endpoints with "instructions", there is only text explaining what can you query for each social media
'''
@app.get('/') 
def home():
    return ('Welcome to General API for Social Media! + list of endpoints and link to readme') # TODO


# TODO: evaluate if we need these
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



# TODO: Add method descriptions

def map_fields(requested_social_media, fields):
    # check which platforms need to be queried based on parameter 'social'
    requested_social_media_data = [] # contains data dictionaries of selected social media platforms
    for social_media in requested_social_media:
        requested_social_media_data.append(data_dictionary[social_media])

    # map fields for similar parameter for each platform
    mapped_fields = [] # contains list of selected fields corresponding to platforms from selected_social_media
    unified_fields = [] # contains list of selected fields (not mapped)
    for social_media in requested_social_media_data:
        temp_fields = ''

        # TODO: Ignore fields that map to empty

        if fields == []: # If no fields are selected, return all possible data
            for field in social_media['field_mapping']:
                #if social_media['field_mapping'][field] != '':
                temp_fields += social_media['field_mapping'][field] + ','
            unified_fields.append(social_media['field_mapping'].keys())
        else:
            for field in fields:
                #if social_media['field_mapping'][field] != '':
                temp_fields += social_media['field_mapping'][field] + ','
            unified_fields = fields
        
        mapped_fields.append(temp_fields[:-1])

    return unified_fields, mapped_fields


def merge_responses(fields, responses):
    merged_response = {}
    merged_response['errors'] = {} # TODO: check if it's better to include 'errors' field only if errors are present
    error_responses, non_error_responses = error_response(responses)

    for field in fields:
        merged_response[field] = []
        for platform in responses:
            temp_dict = {}
            platform_name = data_dictionary[platform]['name']
            temp_dict['provider'] = platform_name
            if platform in non_error_responses:
                specific_field_name = data_dictionary[platform]['field_mapping'][field]
                temp_dict[specific_field_name] = responses[platform].json()[specific_field_name]
                merged_response[field].append(temp_dict)
            else:
                merged_response['errors'][platform_name] = {}
                merged_response['errors'][platform_name]['HTTP_status'] = str(responses[platform])
                merged_response['errors'][platform_name]['json_response'] = responses[platform].json()
                # TODO: check if it's better to include 'errors' field only if errors are present

    response = json.dumps(merged_response, indent=2)
    return response


def error_response(responses):
    error_responses = {}
    non_error_responses = {}
    
    # separate error and non error responses
    for platform in responses:
        if responses[platform].status_code >= 400:
            error_responses[platform] = responses[platform]
        else:
            non_error_responses[platform] = responses[platform]
        
    return error_responses, non_error_responses


###########################################
# Functions for calling social media apis #
###########################################

def call_social_media_APIs(requested_social_media, endpoint, mapped_fields, unified_fields):

    responses = {}

    if 'fb' in requested_social_media:
        fb_response = call_facebook(data_dictionary['fb']['endpoint_mapping'][endpoint], 'fields=' + mapped_fields[requested_social_media.index('fb')], fb_access)
        responses['fb'] = fb_response
        print(fb_response.json())
    
    if 'ig' in requested_social_media:
        ig_response = call_instagram(data_dictionary['ig']['endpoint_mapping'][endpoint], '', ig_token)
        responses['ig'] = ig_response
    
    if 'ln' in requested_social_media:
        ln_headers = create_ln_header(ln_access) # Prepare headers to attach to request
        ln_response = call_linkedin(data_dictionary['ln']['endpoint_mapping'][endpoint], 'fields=' + mapped_fields[requested_social_media.index('ln')], ln_headers)
        responses['ln'] = ln_response
        print(ln_response.json())

    if 'tw' in requested_social_media:
        tw_response = call_twitter(data_dictionary['tw']['endpoint_mapping'][endpoint], '', tw_token)
        responses['tw'] = tw_response

    # merge responses into one json object
    response = merge_responses(unified_fields, responses)
    return response

def call_social_media_APIs_with_given_id(requested_social_media, endpoint, id, mapped_fields, unified_fields):
    responses = {}

    if 'fb' in requested_social_media:
        fb_response = call_facebook(data_dictionary['fb']['endpoint_mapping'][endpoint] + '/' + id, 'fields=' + mapped_fields[requested_social_media.index('fb')], fb_access) # json response
        responses['fb'] = fb_response
        print(fb_response.json())
    
    if 'ig' in requested_social_media:
        ig_response = call_instagram(data_dictionary['ig']['endpoint_mapping'][endpoint] + '/' + id, '', ig_token)
        responses['ig'] = ig_response
    
    if 'ln' in requested_social_media:
        ln_headers = headers(ln_access) # Prepare headers to attach to request
        ln_response = call_linkedin(data_dictionary['ln']['endpoint_mapping'][endpoint] + '/' + id, 'fields=' + mapped_fields[requested_social_media.index('ln')], ln_headers)
        responses['ln'] = ln_response
        print(ln_response.json())

    if 'tw' in requested_social_media:
        tw_response = call_twitter(data_dictionary['tw']['endpoint_mapping'][endpoint] + '/' + id, '', tw_token)
        responses['tw'] = tw_response

    # merge responses into one json object
    response = merge_responses(unified_fields, responses)
    return response

def call_facebook(endpoint, parameters, fb_token):
    base_url = data_dictionary['fb']['base_url']
    if parameters == '':
        response = requests.get(f'{base_url}{endpoint}?&access_token={fb_token}')
    else:
        response = requests.get(f'{base_url}{endpoint}?{parameters}&access_token={fb_token}')
    return response

    # Nested call https://graph.facebook.com/10215963448399509?fields=albums.limit(2){photos.limit(3)}
    # https://graph.facebook.com/NODE?fields=FIRSTLEVEL{SECOND LEVEL} can have even more levels
    # .limit limits the number of returned results

    # graph.facebook.com/me?fields=posts.limit(5){message,privacy{value}}
    # graph.facebook.com/me?fields=albums.limit(5){name,privacy,photos.limit(2){picture}},posts.limit(5){message, privacy}
    

def call_instagram(endpoint, parameters, ig_token):
    base_url = data_dictionary['ig']['base_url']
    response = requests.get(f'{base_url}{endpoint}?{parameters}&access_token={ig_token}')
    return response

def call_linkedin(endpoint, parameters, headers):
    base_url = data_dictionary['ln']['base_url']
    if parameters == '':
        response = requests.get(f'{base_url}{endpoint}', headers = headers)
    else:
        response = requests.get(f'{base_url}{endpoint}?{parameters}', headers = headers)
    return response

def call_twitter(endpoint, parameters, tw_token):
    base_url = data_dictionary['tw']['base_url']
    if parameters == '':
        request = requests.Request(
        'POST', 'https://poloniex.com/tradingApi',
        data=payload, headers=headers)

        with requests.Session() as session:
        response = session.send(prepped)

        response = requests.get(f'{base_url}{endpoint}', headers = headers)
    else:
        response = requests.get(f'{base_url}{endpoint}?{parameters}', headers = headers)
    return response

def check_if_too_many_requested_platforms(requested_social_media):
    if len(requested_social_media) > 1:
        error = {
                    'Error': {
                        'HTTPstatus': 400,
                        'error_code': 1,
                        'message': 'Too many requested social media plaforms. To get elements by id, specify only one social media platform at the time in the parameter \'sm\'.'
                    }
                }
        raise HTTPException(status_code=400, detail=error)
    return

def get_data_with_id(endpoint, id, sm, fields):
    requested_social_media = sm.split(',')
    check_if_too_many_requested_platforms(requested_social_media)
    fields = fields.split(',')

    # map fields
    unified_fields, mapped_fields = map_fields(requested_social_media, fields)

    # perform calls to social media APIs
    response = call_social_media_APIs_with_given_id(requested_social_media, endpoint, id, mapped_fields, unified_fields)
    return response



########################
# Endpoint definitions #
########################

'''
Returns data about the logged-in user specified by parameter 'fields'
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


'''
Returns data about the user with given user_id specified by parameter 'fields'
'''

@app.get('/user/{user_id}')
def get_data_about_user(user_id: str, sm: str = 'fb,ln,tw', fields: str = ''):

    endpoint = 'user'
    response = get_data_with_id(endpoint, user_id, sm, fields)
    return response


'''
Returns data about the post with given post_id specified by parameter 'fields'
'''

@app.get('/post/{post_id}')
def get_data_about_post(post_id: str, sm: str = 'fb,ln,tw', fields: str = ''):
    endpoint = 'post'
    response = get_data_with_id(endpoint, post_id, sm, fields)
    return response


'''
Returns data about the comment with given comment_id specified by parameter 'fields'
'''

@app.get('/comment/{comment_id}')
def get_data_about_post(comment_id: str, sm: str = 'fb,ln,tw', fields: str = ''):
    endpoint = 'comment'
    response = get_data_with_id(endpoint, comment_id, sm, fields)
    return response


# TODO: twitter authentication
# TODO: ln authentication
# TODO: fb authentication
# TODO: unified list of fields (map to empty if field doesn't exist)
# TODO: check if already authenticated
    
    # FURTHER DEVELOPMENT: If too much time, implement parameter "group_by" that allows you to either group by data first or by provider first.
    # FURTHER DEVELOPMENT: When you query, the app checks if all permissions are avaliable and if not it asks you for the permission - aka prompts login and creates access token


# FB CALL EXAMPLES

# graph = facebook.GraphAPI(access_token=token, version = 3.1)
# # events = graph.request('/vanity.name?metadata=1&access_token='+token)
# # print (events)

# page = graph.get_object("Recipes", fields='name,about')
# print (json.dumps(page))




# print(get_data_about_me(sm='fb,ln',fields='id,first_name,last_name'))
# print(get_data_about_user('10215963448399509', 'fb', 'name,id,birthday'))