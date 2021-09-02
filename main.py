# LEGAL
# Facebook: https://developers.facebook.com/devpolicy/
#           https://developers.facebook.com/terms/dfc_platform_terms/
#           https://www.facebook.com/policies_center
# LinkedIn: https://legal.linkedin.com/api-terms-of-use
#           https://www.linkedin.com/legal/user-agreement
# Twitter:  https://developer.twitter.com/en/developer-terms
#           https://twitter.com/en/tos

# OFFICIAL DOCUMENTATION FOR SOCIAL MEDIA APIs
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

from data_dictionaries.Facebook_data import Facebook_data as fbd
from data_dictionaries.Instagram_data import Instagram_data as igd
from data_dictionaries.Linkedin_data import Linkedin_data as lnd
from data_dictionaries.Twitter_data import Twitter_data as twd

from authentication.fb_authentication import auth as fb_auth
from authentication.ig_authentication import auth as ig_auth
from authentication.ln_authentication import auth as ln_auth
from authentication.tw_authentication import auth as tw_auth

from social_media_api_calls.facebook_api_calls import call_api as call_fb_api
from social_media_api_calls.instagram_api_calls import call_api as call_ig_api
from social_media_api_calls.linkedin_api_calls import call_api as call_ln_api
from social_media_api_calls.twitter_api_calls import call_api as call_tw_api


# Instantiate a FastAPI app object
app = FastAPI()

# Create a list of data_dictionaries for social media platforms
data_dictionary = {
    'fb': fbd.dict,
    'ig': igd.dict,
    'ln': lnd.dict,
    'tw': twd.dict
}

# Specify documents with credentials
file_with_fb_credentials = 'fb_credentials.json'
file_with_ig_credentials = 'ig_credentials.json'
file_with_ln_credentials = 'ln_credentials.json'
file_with_tw_credentials = 'tw_credentials.json'

# Authenticate
fb_access = fb_auth(file_with_fb_credentials)

ig_access = ig_auth(file_with_ig_credentials)

ln_access = ln_auth(file_with_ln_credentials)

tw_creds, tw_error = tw_auth(file_with_tw_credentials)
if tw_error != None:
    tw_access = tw_creds
    print(tw_error, tw_error.json)
    # TODO: raise Exception or somehow include tw_error in a merged response

tw_access = tw_creds



def error_response(responses):
    ''' Checks if any of responses are error responses and if so, separates them from the others. 
    
    Parameters
    -----
    responses: dict
        Dictionary of responses from all social media APIs that were called.

    Returns
    -----
    dict, dict
        Returns two dictionaries (`error_responses`, `non_error_responses`) with the following format: 
        {'short name of social media platform (string)': requests.Response object}
    '''

    error_responses = {}
    non_error_responses = {}
    
    # separate error and non error responses
    for platform in responses:
        if responses[platform].status_code >= 400:
            error_responses[platform] = responses[platform]
        else:
            non_error_responses[platform] = responses[platform]
        
    return error_responses, non_error_responses


def merge_responses(unified_fields, responses):
    ''' Compiles responses of social media APIs into one json response. 
    
    Parameters
    -----
    unified_fields: list
        List of all fields that were requested or are default.
    responses: dict
        Dictionary of responses from all social media APIs that were called.

    Returns
    -----
    string
        Returns json string with a compiled response.
    '''

    merged_response = {}
    merged_response['errors'] = {}

    # Separate error and non error responses
    error_responses, non_error_responses = error_response(responses)

    # Merge responses
    for field in unified_fields:
        merged_response[field] = []
        for platform in responses:
            temp_dict = {}
            platform_name = data_dictionary[platform]['name']
            
            if platform in non_error_responses:
                specific_field_name = data_dictionary[platform]['field_mapping'][field]
                if specific_field_name == None:
                    continue
                temp_dict['provider'] = platform_name
                temp_dict[specific_field_name] = responses[platform].json()[specific_field_name]
                merged_response[field].append(temp_dict)
            else:
                merged_response['errors'][platform_name] = {}
                merged_response['errors'][platform_name]['HTTP_status'] = str(responses[platform])
                merged_response['errors'][platform_name]['json_response'] = responses[platform].json()
                
    # Convert dictionary merged_responses to json string
    response = json.dumps(merged_response, indent=2)
    return response


def map_fields(requested_social_media, fields):
    ''' Compiles responses of social media APIs into one json response. 
    
    Parameters
    -----
    requested_social_media: list
        List of short names for social media platforms that were requested via parameter 'sm'. Assumes that there is at least 1 element in the list.
    fields: list
        List of all fields that were requested.

    Returns
    -----
    list, list
        Returns two lists: `mapped_fields` and `unified_fields`. `mapped_fields` contains list of selected fields corresponding to requested social media platforms from `selected_social_media`. `unified_fields` contains list of selected fields (not mapped). If parameter `fields` is empty, `unified_fields` contains all possible fields.
    '''

    # contains data dictionaries of selected social media platforms
    requested_social_media_data = [] 

    # check which platforms need to be queried based on parameter 'social'
    for social_media in requested_social_media:
        requested_social_media_data.append(data_dictionary[social_media])

    # contains list of selected fields corresponding to platforms from selected_social_media
    mapped_fields = []

    # contains list of selected fields (not mapped)
    unified_fields = fields

    # If no fields are selected, return all possible data
    if fields == []: 
        unified_fields = requested_social_media_data.keys()[0]['field_mapping'].keys()

    # Map fields for similar parameter for each platform
    for social_media in requested_social_media_data:
        temp_fields = ''

        if fields == []: 
            # Collate all possible fields
            for field in social_media['field_mapping']:
                if social_media['field_mapping'][field] != None:
                    temp_fields += social_media['field_mapping'][field] + ','
        else:
            # Collate requested fields
            for field in fields:
                if social_media['field_mapping'][field] != None:
                    temp_fields += social_media['field_mapping'][field] + ','
            
        # Add mapped fields to the list
        mapped_fields.append(temp_fields[:-1])

    return unified_fields, mapped_fields


def call_social_media_APIs(requested_social_media, endpoint, fields, id=None):
    ''' Calls socaila media APIs. 
    
    Parameters
    -----
    requested_social_media: list
        List of short names for social media platforms that were requested via parameter 'sm'. Assumes that there is at least 1 element in the list.
    endpoint: string
        String containing the endpoint that was called.
    fields: list
        List of all fields that were requested.
    id: string
        Optional parameter with default value of `None`. If provided, it is a string identifying a certain object from a social media platform. If this parameter is provided, there will be exactly 1 element in the `requested_social_media` list.

    Returns
    -----
    string
        Returns json string with a single response that consists of merged responses of social media APIs. 
    '''

    responses = {}

    # map fields
    fields = fields.split(',')
    unified_fields, mapped_fields = map_fields(requested_social_media, fields)

    # call social media APIs
    if 'fb' in requested_social_media:
        responses['fb'] = call_fb_api(fb_access, data_dictionary['fb'], endpoint, mapped_fields[requested_social_media.index('fb')], id) # fb_api or fb_access
    
    if 'ig' in requested_social_media:
        responses['ig'] = call_ig_api(ig_api, data_dictionary['ig'], endpoint, mapped_fields[requested_social_media.index('ig')], id) # ig_api or ig_access
    
    if 'ln' in requested_social_media:
        responses['ln'] = call_ln_api(ln_access, data_dictionary['ln'], endpoint, mapped_fields[requested_social_media.index('ln')], id)

    if 'tw' in requested_social_media:
        responses['tw'] = call_tw_api(tw_api, data_dictionary['tw'], endpoint, mapped_fields[requested_social_media.index('tw')], id)

    # merge responses into one json object
    response = merge_responses(unified_fields, responses)
    return response


def check_if_too_many_requested_platforms(requested_social_media):
    ''' Checks if there is more than 1 requested social media platform in the request. 
    
    Parameters
    -----
    requested_social_media: list
        List of short names for social media platforms that were requested via parameter 'sm'. Assumes that there is at least 1 element in the list.

    Raises HTTPexception if there is more than 1 requested social media.
    '''

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


def call_social_media_APIs_with_id(sm, endpoint, fields, id):
    ''' Calls socaila media APIs. 
    
    Parameters
    -----
    sm: string
        String containing value of `sm` parameter form the request.
    endpoint: string
        String containing the endpoint that was called.
    fields:
        List of all fields that were requested.
    id: string
        String identifying a certain object from a social media platform.

    Returns
    -----
    string
        Returns json string with a single response that consists of merged responses of social media APIs. 
    '''

    requested_social_media = sm.split(',')
    check_if_too_many_requested_platforms(requested_social_media)

    response = call_social_media_APIs(requested_social_media, endpoint, fields, id=id)
    return response


########################
# Endpoint definitions #
########################

@app.get('/') 
def home():
    
    return ('Welcome to General API for Social Media! + list of endpoints and link to readme') # TODO


@app.get('/me')
def get_data_about_me(sm: str, fields: str = ''):
    '''Returns data about the logged-in user specified by parameter `fields`'''

    endpoint = 'me'
    requested_social_media = sm.split(',')
    response = call_social_media_APIs(requested_social_media, endpoint, fields)
    return response


@app.get('/user/{user_id}')
def get_data_about_user(user_id: str, sm: str, fields: str = ''):
    '''Returns data about the user with given user_id specified by parameter `fields`'''

    endpoint = 'user'
    response = call_social_media_APIs_with_id(sm, endpoint, fields, user_id)
    return response


@app.get('/post/{post_id}')
def get_data_about_post(post_id: str, sm: str, fields: str = ''):
    '''Returns data about the post with given user_id specified by parameter `fields`'''

    endpoint = 'post'
    response = call_social_media_APIs_with_id(sm, endpoint, fields, post_id)
    return response


@app.get('/comment/{comment_id}')
def get_data_about_comment(comment_id: str, sm: str, fields: str = ''):
    '''Returns data about the comment with given user_id specified by parameter `fields`'''

    endpoint = 'comment'
    response = call_social_media_APIs_with_id(sm, endpoint, fields, comment_id)
    return response


# TODO: twitter authentication
# TODO: ln authentication
# TODO: fb authentication
# TODO: check if already authenticated
# TODO: error handling if no social media is selected
# TODO: iclude HTTP status codes in merged response
# TODO: limit parameter (how many items do you want returned)
# TODO: check error handling of the "too many requested social media platforms" error
# TODO: error handling for twitter authentication failure: raise Exception or somehow include tw_error in a merged response
# TODO: create method for authentication that checks validity of all credentials, maybe /authenticate and/or /authenticate/sm_name
# TODO: write welcome message and quick how to for the homepage on index

# TODO: add empty files for credentials to github

# FURTHER DEVELOPMENT: If too much time, implement parameter "group_by" that allows you to either group by data first or by provider first.
# FURTHER DEVELOPMENT: When you query, the app checks if all permissions are avaliable and if not it asks you for the permission - aka prompts login and creates access token


# QUICK TEST
print(get_data_about_me(sm='fb,ln',fields='id,first_name,last_name,birthday'))
print(get_data_about_user('10215963448399509', 'fb', 'name,id,birthday'))