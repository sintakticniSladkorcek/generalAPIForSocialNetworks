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

from fastapi import FastAPI, HTTPException, Query
import facebook # TODO: Do we need this library?
import tweepy # TODO: Do we need this library?
import json
import requests
import inspect

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

fb_access = ig_access = ln_access = tw_access = None
fb_authenticated = ig_authenticated = ln_authenticated = tw_authenticated = False

fields_dictionary = {
    'get': 'get_fields',
    'post': 'post_fields',
    'delete': 'delete_fields'
}


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


def merge_responses(method, endpoint, unified_fields, responses):
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

    # Merge responses for GET method
    if method == 'get':
        for field in unified_fields:
            merged_response[field] = []
            for platform in responses:
                temp_dict = {}
                platform_name = data_dictionary[platform]['name']
                
                if platform in non_error_responses:
                    specific_field_name = data_dictionary[platform]['endpoint_mapping'][endpoint]['get_fields'][field]
                    if specific_field_name == None:
                        continue
                    temp_dict['provider'] = platform_name
                    temp_dict[specific_field_name] = responses[platform].json()[specific_field_name]
                    merged_response[field].append(temp_dict)
                else:
                    merged_response['errors'][platform_name] = {}
                    merged_response['errors'][platform_name]['HTTP_status'] = str(responses[platform])
                    merged_response['errors'][platform_name]['json_response'] = responses[platform].json()
    
    # Merge responses for POST method
    elif method == 'post':
        for platform in responses:
            platform_name = data_dictionary[platform]['name']
           
            if platform in non_error_responses:
                merged_response[platform_name] = responses[platform].json()
            else:
                merged_response['errors'][platform_name] = {}
                merged_response['errors'][platform_name]['HTTP_status'] = str(responses[platform])
                merged_response['errors'][platform_name]['json_response'] = responses[platform].json()
                
    # Convert dictionary merged_responses to json string
    response = merged_response
    return response


def map_fields(method, requested_social_media, endpoint, path, fields):
    ''' Compiles responses of social media APIs into one json response. 
    
    Parameters
    -----
    method: string
        String denoting a HTTP method. One of 'get', 'post', 'delete'.
    requested_social_media: list
        List of short names for social media platforms that were requested via parameter 'sm'. Assumes that there is at least 1 element in the list.
    endpoint: string
        Endpoint to which the request will be addressed.
    fields: string or dictionary
        For GET method: string of fields separated by commas
        For POST method: dictionary of field_name - field_value pairs

    Returns
    -----
    list, list
        Returns two lists: `unified_fields` and `mapped_fields`.
        For GET method: `unified_fields` contains list of all requested fields (not mapped). If parameter `fields` is empty, `unified_fields` contains all possible fields. `mapped_fields` contains list of concatenated strings of selected fields corresponding to requested social media platforms from `selected_social_media` separated by commas.
        For POST method: `unified_fields` contains list of all requested fields (not mapped). `mapped_fields` contains list of dictionaries corresponding to requested social media platforms from `selected_social_media`, dictionaries contain social_media_specific_field_name - field_value pairs.
    '''

    # chooses the field mapping
    type_of_fields = fields_dictionary[method]

    # prepare fields for processing for the GET method
    if method=='get' and fields != None:
        prepared_fields = fields.split(',')

    # prepare fields for processing for the POST method
    elif method=='post':
        prepared_fields = fields.keys()

    # contains data dictionaries of selected social media platforms
    requested_social_media_data = [] 

    # check which platforms need to be queried based on parameter 'social'
    for social_media in requested_social_media:
        requested_social_media_data.append(data_dictionary[social_media])

    # contains list of selected fields corresponding to platforms from selected_social_media
    mapped_fields = []

    # contains list of selected fields (not mapped)
    unified_fields = prepared_fields

    # If no fields are selected, return all possible data
    if fields == [''] or fields == None: # TODO: Check if we need also the [''] option 
        unified_fields = requested_social_media_data[0]['endpoint_mapping'][endpoint][type_of_fields].keys()

    
    # Map fields for similar parameter for each platform
    for social_media in requested_social_media_data:

        # Map for GET method
        if method == 'get': # TODO: Move concatenating to files for social medi API calls
            temp_fields = ''
            if fields == [''] or fields == None: # TODO: Check if we need also the [''] option
                # Collate all possible fields
                for field in social_media['endpoint_mapping'][endpoint][type_of_fields]:
                    if social_media['endpoint_mapping'][endpoint][type_of_fields][field] != None:
                        temp_fields += social_media['endpoint_mapping'][endpoint][type_of_fields][field] + ','
            else:
                # Collate requested fields
                for field in unified_fields:
                    if social_media['endpoint_mapping'][endpoint]['get_fields'][field] != None:
                        temp_fields += social_media['endpoint_mapping'][endpoint]['get_fields'][field] + ','
                
            # Add mapped fields to the list
            mapped_fields.append(temp_fields[:-1])

        # Map for POST method
        elif method == 'post':
            temp_fields = {}
            for field in unified_fields:
                if social_media['endpoint_mapping'][endpoint]['get_fields'][field] != None:
                    temp_fields[social_media['endpoint_mapping'][endpoint]['get_fields'][field]] = fields[field]
            
            # Add mapped fields to the list
            mapped_fields.append(temp_fields)

    print('unified_fields', unified_fields, 'mapped_fields', mapped_fields)
    return unified_fields, mapped_fields


def call_social_media_APIs(method, requested_social_media, endpoint, path, id=None, fields=None):
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

    # check if value of the 'sm' field is valid
    check_if_valid_platforms_requested(requested_social_media, list(data_dictionary.keys()))

    # map fields
    if method=='get' and fields != None:
        fields = fields.split(',')
    unified_fields, mapped_fields = map_fields(method, requested_social_media, endpoint, path, fields) # TODO: make path dependent!

    # call social media APIs
    if 'fb' in requested_social_media:
        # if not fb_authenticated:
        #     authenticate('fb')
        responses['fb'] = call_fb_api(fb_access, data_dictionary['fb'], method, endpoint, path, mapped_fields[requested_social_media.index('fb')], id) # fb_api or fb_access
    
    if 'ig' in requested_social_media:
        # if not ig_authenticated:
        #     authenticate('ig')
        responses['ig'] = call_ig_api(ig_api, data_dictionary['ig'], method, endpoint, path, mapped_fields[requested_social_media.index('ig')], id) # ig_api or ig_access
    
    if 'ln' in requested_social_media:
        # if not ln_authenticated:
        #     authenticate('ln')
        responses['ln'] = call_ln_api(ln_access, data_dictionary['ln'], method, endpoint, path, mapped_fields[requested_social_media.index('ln')], id)

    if 'tw' in requested_social_media:
        # if not tw_authenticated:
        #     authenticate('tw')
        responses['tw'] = call_tw_api(tw_api, data_dictionary['tw'], method, endpoint, path, mapped_fields[requested_social_media.index('tw')], id)

    # merge responses into one json object
    response = merge_responses(method, endpoint, unified_fields, responses)
    return response


def check_if_valid_platforms_requested(requested_social_media, supported_social_media):
    ''' Checks if requested social media platforms are supported. 
    
    Parameters
    -----
    requested_social_media: list
        List of short names for social media platforms that were requested via parameter 'sm'.
    supported_social_media: list
        List of all social media platforms that are currently supported.

    Raises HTTPexception if an invalid social media platform is requested.
    '''
    for social_media in requested_social_media:
        if social_media not in supported_social_media:
            error = {
                'Error': {
                    'HTTPstatus': 400,
                    'error_code': 2,
                    'message': f'\'{social_media}\' is not a valid value for the parameter \'sm\'. Please choose among the supported values: {supported_social_media}'
                }
            }
            raise HTTPException(status_code=400, detail=error)
    return


def check_if_too_many_requested_platforms(requested_social_media):
    ''' Checks if there is more than 1 requested social media platform in the request. 
    
    Parameters
    -----
    requested_social_media: list
        List of short names for social media platforms that were requested via parameter 'sm'.

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


def call_social_media_APIs_with_id(method, sm, endpoint, path, id, fields=None):
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

    response = call_social_media_APIs(method, requested_social_media, endpoint, path, id=id, fields=fields)
    return response


def actual_kwargs():
    """
    Decorator that provides the wrapped function with an attribute 'actual_kwargs'
    containing just those keyword arguments actually passed in to the function.
    """
    def decorator(function):
        def inner(*args, **kwargs):
            inner.actual_kwargs = kwargs
            return function(*args, **kwargs)
        return inner
    return decorator


########################
# Endpoint definitions #
########################

# GET requests

@app.get('/') 
def home():
    response = requests.Response()
    response.status_code = 200
    response.json = {'Hello': 'Welcome to General API for Social Networks! Check out documentation on /docs, /redoc or on Github https://github.com/sintakticniSladkorcek/generalAPIForSocialNetworks.'}
    return (response)


@app.get('/auth')
def authenticate(sm: str):

    requested_social_media = sm.split(',')

    response = {}

    # authenticate with social media APIs
    if 'fb' in requested_social_media:
        try:
            global fb_access
            fb_access = fb_auth(file_with_fb_credentials)
            fb_authenticated = True
            response['Facebook'] = 'Success'
        except:
            response['Facebook'] = 'Error'
    
    if 'ig' in requested_social_media:
        try:
            global ig_access
            ig_access = ig_auth(file_with_ig_credentials)
            ig_authenticated = True
            response['Instagram'] = 'Success'
        except:
            response['Instagram'] = 'Error'
    
    if 'ln' in requested_social_media:
        try:
            global ln_access
            ln_access = ln_auth(file_with_ln_credentials)
            ln_authenticated = True
            response['LinkedIn'] = 'Success'
        except:
            response['LinkedIn'] = 'Error'

    if 'tw' in requested_social_media:
        tw_creds, tw_error = tw_auth(file_with_tw_credentials)
        if tw_error != None:
            global tw_access
            tw_access = tw_creds
            print(tw_error, tw_error.json)
            response['Twitter'] = 'Error'
            # TODO: raise Exception or somehow include tw_error in a merged response
        tw_authenticated = True
        response['Twitter'] = 'Success'

    return response

# fb: fields, permissions and error codes: https://developers.facebook.com/docs/graph-api/reference/album
@app.get('/album/{album_id}')
def get_data_abut_album(album_id: str, sm: str, fields: str = ''):
    '''Returns data about the album with given album_id specified by parameter `fields`'''

    endpoint = 'album'
    method = 'get'
    response = call_social_media_APIs_with_id(method, sm, endpoint, '', album_id, fields=fields)
    return response


# fb: fields, permissions, updating rules, errors https://developers.facebook.com/docs/graph-api/reference/v11.0/comment
@app.get('/comment/{comment_id}')
def get_data_about_comment(comment_id: str, sm: str, fields: str = ''):
    '''Returns data about the comment with given user_id specified by parameter `fields`'''

    endpoint = 'comment'
    method = 'get'
    response = call_social_media_APIs_with_id(method, sm, endpoint, '', comment_id, fields=fields)
    return response


# fb:
@app.get('/event/{event_id}')
def get_data_about_event(event_id: str, sm: str, fields: str = ''):
    '''Returns data about the event with given event_id specified by parameter `fields`'''

    endpoint = 'event'
    method = 'get'
    response = call_social_media_APIs_with_id(method, sm, endpoint, '', event_id, fields=fields)
    return response


# fb
@app.get('/group/{group_id}')
def get_data_about_group(group_id: str, sm: str, fields: str = ''):
    '''Returns data about the group with given group_id specified by parameter `fields`'''

    endpoint = 'group'
    method = 'get'
    response = call_social_media_APIs_with_id(method, sm, endpoint, '', group_id, fields=fields)
    return response


# fb
@app.get('/live_video/{video_id}')
def get_data_about_live_video(video_id: str, sm: str, fields: str = ''):
    '''Returns data about the live video with given video_id specified by parameter `fields`'''

    endpoint = 'live_video'
    method = 'get'
    response = call_social_media_APIs_with_id(method, sm, endpoint, '', video_id, fields=fields)
    return response


# fb, ln, tw
@app.get('/me')
def get_data_about_me(sm: str, fields: str = ''):
    '''Returns data about the logged-in user specified by parameter `fields`'''

    endpoint = 'me'
    method = 'get'
    requested_social_media = sm.split(',') # Because this endpoint is not id dependent
    response = call_social_media_APIs(method, requested_social_media, endpoint, '', fields=fields)
    return response


# fb
@app.get('/post/{post_id}')
def get_data_about_post(post_id: str, sm: str, fields: str = ''):
    '''Returns data about the post with given user_id specified by parameter `fields`'''

    endpoint = 'post'
    method = 'get'
    response = call_social_media_APIs_with_id(method, sm, endpoint, '', post_id, fields=fields)
    return response


# fb
@app.get('/user/{user_id}')
def get_data_about_user(user_id: str, sm: str, fields: str = ''):
    '''Returns data about the user with given user_id specified by parameter `fields`'''

    endpoint = 'user'
    method = 'get'
    response = call_social_media_APIs_with_id(method, sm, endpoint, '', user_id, fields=fields)
    return response


# POST requests

# TODO: setup mappings
# fb: fields:https://developers.facebook.com/docs/graph-api/reference/album
# Privacy levels (enum, fb name, our name)
# * level 0 ==>only me (me)
# * level 1==>friend only (connections)
# * level 2==>public (public)
# * level >2 ==>error
@actual_kwargs()
@app.post('group/{group_id}/album')
def create_album_in_group(group_id:str, sm:str, name: str, description: str, visible_to: str='connections', make_shared_album: bool=False, contributors: list=None, location_by_page_id: str=None, location_by_name: str=None):
    ''' Creates a new album in a group specified by group_id '''

    endpoint = 'group'
    path = 'album'
    method = 'post'

    fields = create_album_in_group.actual_kwargs
    del fields['group_id']
    del fields['sm']

    response = call_social_media_APIs_with_id(method, sm, endpoint, path, group_id, fields=fields)
    return response


# # TODO
# #fb: fields, permissions, errors https://developers.facebook.com/docs/graph-api/reference/v11.0/comment
# @app.post('album/{album_id}/comment')
# def comment_on_album(album_id:str, sm:str, TODO:todo):
#     ''' Posts a comment on the album specified by album_id '''

#     endpoint = 'album'
#     path = 'comment'
        # method = 'post'
#     requested_social_media = sm.split(',')
#     response = None # TODO
#     return response

# # TODO: Maybe set path to reply instead of comment
# @app.post('comment/{comment_id}/comment')
# def reply_to_comment(comment_id:str, sm:str, TODO:todo):
#     ''' Reply to a comment with comment_id '''

#     endpoint = 'comment'
#     path = 'comment'
#       method = 'post'
#     requested_social_media = sm.split(',')
#     response = None # TODO
#     return response

# @app.post('event/{event_id}/comment')
# @app.post('link/{link_id}/comment')
# @app.post('live_video/{video_id}/comment')
# @app.post('photo/{photo_id}/comment')
# @app.post('post/{post_id}/comment')
# @app.post('thread/{thread_id}/comment')
# @app.post('user/{user_id}/comment')
# @app.post('video/{video_id}/comment')


# fb
@app.post('/live_video/{video_id}')
def update_live_video(
    video_id: str, 
    sm: str, 

    allow_bm_crossposting: bool=None,

    content_tags: list=None, 

    crossposting_actions: list=None,
    custom_labels: list=None,

    description: str=None, 

    direct_share_status: int=None,
    disturbing: bool=None,

    donate_button_charity_id: str=None, 

    embeddable: bool=None,
    end_live_video: bool=None,
    is_manual_mode: bool=None,
    live_comment_moderation_setting: list=None,

    live_encoders: list=None, 

    master_ingest_stream_id: str=None,
    location: str=None,

    planned_start_time: int=None,
    visible_to: str='connections',
    projection: str='eqirectangular',
    custom_image_for_schedule: str=None,

    custom_background_image_for_schedule: str=None,
    sponsor_id: str=None,
    sponsor_relationship: int=None,

    status: str='unpublished',

    tagged_users: list=None,
    targeting: str=None,

    video_title: str=Query(None, max_length=254)
    ):
    '''Creates a live video on users profile with given user_id.'''

    endpoint = 'user'
    method = 'post'
    response = None # TODO
    return response


# fb
@app.post('/user/{user_id}/live_video')
def create_live_video_on_user(
    user_id: str, 
    sm: str, 
    app_id: str, 
    content_tags: list=None, 
    description: str=None, 
    donate_button_charity_id: str=None, 
    enable_backup_ingest: bool=False, 
    encoding_settings_identifier: str=None, 
    fisheye_video_cropped: bool=None, 
    front_z_rotation: float=None, 
    is_360: bool=False, 
    live_encoders: list=None, 
    original_fov: int=None,
    planned_start_time: int=None,
    visible_to: str='connections',
    projection: str='eqirectangular',
    custom_image_for_schedule: str=None,
    spatial_audio_format: int=None,
    status: str='unpublished',
    stereoscopic_mode: str='mono',
    stop_on_delete_stream: bool=False,
    video_title: str=Query(None, max_length=254)
    ):
    '''Creates a live video on users profile with given user_id.'''

    endpoint = 'user'
    method = 'post'
    response = None # TODO
    return response


# fb
@app.post('/group/{group_id}/live_video')
def create_live_video_in_group(
    group_id: str, 
    sm: str, 
    app_id: str, 
    content_tags: list=None, 
    description: str=None, 
    enable_backup_ingest: bool=False, 
    encoding_settings_identifier: str=None, 
    fisheye_video_cropped: bool=None, 
    front_z_rotation: float=None, 
    is_360: bool=False, 
    live_encoders: list=None, 
    original_fov: int=None,
    planned_start_time: int=None,
    visible_to: str='connections',
    projection: str='eqirectangular',
    custom_image_for_schedule: str=None,
    spatial_audio_format: int=None,
    status: str='unpublished',
    stereoscopic_mode: str='mono',
    stop_on_delete_stream: bool=False,
    video_title: str=Query(None, max_length=254)
    ):
    '''Creates a live video in group with given group_id.'''

    endpoint = 'group'
    method = 'post'
    response = None # TODO
    return response


# fb
@app.post('/page/{page_id}/live_video')
def create_live_video_on_page(
    page_id: str, 
    sm: str, 
    app_id: str, 
    content_tags: list=None, 
    crossposting_actions: list=None,
    custom_labels: list=None,
    description: str=None, 
    donate_button_charity_id: str=None, 
    enable_backup_ingest: bool=False, 
    encoding_settings_identifier: str=None, 
    fisheye_video_cropped: bool=None, 
    front_z_rotation: float=None, 
    game_show: str=None,
    is_360: bool=False, 
    live_encoders: list=None, 
    original_fov: int=None,
    planned_start_time: int=None,
    visible_to: str='connections',
    products_shown: list=None,
    projection: str='eqirectangular',
    custom_image_for_schedule: str=None,
    spatial_audio_format: int=None,
    status: str='unpublished',
    stereoscopic_mode: str='mono',
    stop_on_delete_stream: bool=False,
    targeting: str=None,
    video_title: str=Query(None, max_length=254)
    ):
    '''Creates a live video on users profile with given user_id.'''

    endpoint = 'user'
    method = 'post'
    response = None # TODO
    return response


# fb
@app.post('/event/{event_id}/live_video')
def create_live_video_in_event(
    event_id: str, 
    sm: str, 
    app_id: str, 
    content_tags: list=None, 
    description: str=None, 
    enable_backup_ingest: bool=False, 
    encoding_settings_identifier: str=None, 
    fisheye_video_cropped: bool=None, 
    front_z_rotation: float=None, 
    is_360: bool=False, 
    live_encoders: list=None, 
    original_fov: int=None,
    planned_start_time: int=None,
    visible_to: str='connections',
    projection: str='eqirectangular',
    custom_image_for_schedule: str=None,
    spatial_audio_format: int=None,
    status: str='unpublished',
    stereoscopic_mode: str='mono',
    stop_on_delete_stream: bool=False,
    video_title: str=Query(None, max_length=254)
    ):
    '''Creates a live video in event with given event_id.'''

    endpoint = 'user'
    method = 'post'
    response = None # TODO
    return response




# DELETE requests

#fb: fields, permissions, errors https://developers.facebook.com/docs/graph-api/reference/v11.0/comment
@app.delete('/comment/{comment_id}')
def delete_comment(comment_id: str, sm: str):
    '''Delete a comment with the given id'''

    endpoint = 'comment'
    method = 'delete'
    response = None # TODO
    return response


#fb
@app.delete('/live_video/{video_id}')
def delete_live_video(video_id: str, sm: str):
    '''Delete a live video with the given video_id'''

    endpoint = 'live_video'
    method = 'delete'
    response = None # TODO
    return response



# TODO: Add this type (fb): /search?type=adinterest&q=TEDx
# {id}/reactions and likes


# TODO: Finish adding /comment endpoints
# TODO: include HTTP status codes in merged response
# TODO: Add paths like /feed or /timeline for /user endpoint
# TODO: limit parameter (how many items do you want returned)
# TODO: API calls for post requests
# TODO: API calls for delete requests


# TODO: twitter authentication (maybe even offer login with bearer token in addition to user login)
# TODO: ln authentication, https://stackoverflow.com/questions/13522497/what-is-oob-in-oauth (also relevant for Twitter)
# TODO: fb authentication
# TODO: check if already authenticated
# TODO: error handling for twitter authentication failure: raise Exception or somehow include tw_error in a merged response
# TODO: create method for authentication that checks validity of all credentials, maybe /authenticate and/or /authenticate/sm_name
# TODO: For the fb app to make it usable to non-authors, we need to implement Facebook Data Deletion Callback: https://developers.facebook.com/docs/development/build-and-test
# TODO: Refresh Facebook user access token (otherwise it my expire in 2 hours)

# TODO: Is it enough to support user-accessible APIs or do I need markting ones too? (Instagram basic display API vs Instagram Graph API) (Facebook Graph API vs Facebook Marketing API vs Facebook ads API), see "For example, user-related permissions are not available to Business apps, and business-related permissions are not available to Consumer apps." from https://developers.facebook.com/docs/development/build-and-test
# TODO: Add restrictions/errors for functionalities that are only applicable to some social media APIs: each function has list of supported social media? And later we change to some more elaborate solution?
# TODO: Add mapping of the privacy values https://developers.facebook.com/docs/graph-api/reference/privacy/
# TODO: Add more fb endpoints
# TODO: Add Twitter endpoints and mappings
# TODO: Add LinkedIn endpoints and mappings
# TODO: Add Instagram authentication
# TODO: Add Instagram endpoints and mappings

# FURTHER DEVELOPMENT: Right now, you cannot authenticate only some social media APIs, you HAVE to authenticate all to be able to use the api at all. Also now all of the data has to be saved in files, maybe it would be better to make it so that all the neccessary data is passed via call to /auth.
# FURTHER DEVELOPMENT: If too much time, implement parameter "group_by" that allows you to either group by data first or by provider first.
# FURTHER DEVELOPMENT: When you query, the app checks if all permissions are avaliable and if not it asks you for the permission - aka prompts login and creates access token
# FURTHER DEVELOPMENT: Beginning with SDK v13.0 for iOS and Android, set to release in early 2022, a Client Token will be required for all calls to the Graph API. https://developers.facebook.com/docs/facebook-login/access-tokens/
# FURTHER DEVELOPMENT: Add suggestions on how to resolve the error in the merged response. Either from the docs of social media APIs or from us if it's something with this api.
# FURTHER DEVELOPMENT: expansion/multiple requests in one https://developers.facebook.com/docs/graph-api/field-expansion/
# FURTHER DEVELOPMENT: Add Facebook's edges also as endpoints, not just as fields
# FURTHER DEVELOPMENT: Create data dictionaries on the go from csv tables for each endpoint (easier to update/add/remove an endpoint or field)


# QUICK TEST
authenticate('fb')
# print(get_data_about_me(sm='fb,ln',fields='id,first_name,last_name,birthday'))
print(create_album_in_group(group_id= '2998732937039201', sm='fb', name='test1', description='lalala'))
# 2998732937039201
# print(get_data_about_user('10215963448399509', 'fb', 'name,id,birthday'))