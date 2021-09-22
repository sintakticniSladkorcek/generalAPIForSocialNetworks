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
import inspect
import asyncio
import requests
from requests import Response
from hypercorn.config import Config
from hypercorn.asyncio import serve

from data_dictionaries.Facebook_data import Facebook_data as fbd
from data_dictionaries.Instagram_data import Instagram_data as igd
from data_dictionaries.Linkedin_data import Linkedin_data as lnd
from data_dictionaries.Twitter_data import Twitter_data as twd

from authentication.fb_authentication import auth as fb_auth
from authentication.ig_authentication import auth as ig_auth
from authentication.ln_authentication import auth as ln_auth
from authentication.tw_authentication import auth as tw_auth
from authentication.ig_authentication import auth_part_2 as ig_auth_2
from authentication.ln_authentication import auth_part_2 as ln_auth_2

from social_media_api_calls.facebook_api_calls import call_api as call_fb_api
from social_media_api_calls.instagram_api_calls import call_api as call_ig_api
from social_media_api_calls.linkedin_api_calls import call_api as call_ln_api
from social_media_api_calls.twitter_api_calls import call_api as call_tw_api

# Set up hypercorn
hypercorn_config = Config()
hypercorn_config.certfile = 'cert.pem'
hypercorn_config.keyfile = 'key.pem'
hypercorn_config.bind = ['localhost:443']

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
    'post': 'post_fields'
}


def resolve_pagination(items):
    '''

    '''
    all_items = []

    while(True):
        try:
            for item in items['data']:
                all_items.append(item)
            # Attempt to make a request to the next page of data, if it exists.
            items=requests.get(items['paging']['next']).json()
        except KeyError:
            # When there are no more pages (['paging']['next']), break from the
            # loop and end the script.
            break
    return all_items


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


def merge_responses(method, endpoint, unified_fields, responses, limit):
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
                    try:
                        field_data = responses[platform].json()[specific_field_name]
                        if 'paging' in field_data:
                            if 'next' in field_data['paging']:
                                all_data = resolve_pagination(field_data)
                                field_data['data'] = all_data
                        
                        limit_exists = limit != None
                        if limit_exists:
                            try:
                                limit = json.loads(limit)
                                
                                field_matches = field in limit    # limit['field'] == field
                                count_ok = limit[field] > 0     # limit['count'] > 0
                                if limit_exists and field_matches and count_ok:
                                    field_data['data'] = field_data['data'][:int(limit[field])]
                            except:
                                error = {
                                    'Error': {
                                        'HTTPstatus': 400,
                                        'error_code': 3,
                                        'message': limit + ' is not a valid value. limit[\'<name_of_the_field>\'] must be an integer. Please use the following format for the \'limit\' parameter: {"<name_of_the_field>":<integer>}'
                                    }
                                }
                                raise HTTPException(status_code=400, detail=error)
                                
                        temp_dict[specific_field_name] = field_data    
                        merged_response[field].append(temp_dict)
                    except HTTPException:
                        response = Response()
                        response.status_code = 400
                        response.reason = error['Error']['message']
                        response.json = error
                        return response
                    except:
                        continue
                    

                else:
                    merged_response['errors'][platform_name] = {}
                    merged_response['errors'][platform_name]['HTTP_status'] = str(responses[platform])
                    try:
                        merged_response['errors'][platform_name]['json_response'] = responses[platform].json()
                    except:
                        merged_response['errors'][platform_name]['json_response'] = responses[platform]
    # Merge responses for POST method and DELETE method
    elif method == 'post' or method == 'delete':
        for platform in responses:
            platform_name = data_dictionary[platform]['name']
           
            if platform in non_error_responses:
                merged_response[platform_name] = responses[platform].json()
            else:
                merged_response['errors'][platform_name] = {}
                merged_response['errors'][platform_name]['HTTP_status'] = str(responses[platform])
                try:
                    merged_response['errors'][platform_name]['json_response'] = responses[platform].json()
                except:
                    merged_response['errors'][platform_name]['json_response'] = responses[platform]
                
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

    # Skip all of this if the method is DELETE
    if method == 'delete':
        return None, None

    # chooses the field mapping
    type_of_fields = fields_dictionary[method]

    # prepare fields for processing for the GET method
    if method=='get':
        if fields != None:
            prepared_fields = fields.split(',')
        else:
            prepared_fields = None
    

    # prepare fields for processing for the POST method
    elif method=='post':
        if fields != None:
            prepared_fields = fields.keys()
        else:
            prepared_fields = None

    # contains data dictionaries of selected social media platforms
    requested_social_media_data = [] 

    # check which platforms need to be queried based on parameter 'social'
    for social_media in requested_social_media:
        requested_social_media_data.append(data_dictionary[social_media])

    # contains list of selected fields corresponding to platforms from selected_social_media
    mapped_fields = {}

    # contains list of selected fields (not mapped)
    unified_fields = prepared_fields

    # set location of field mappings for unified_fields depending on presence of path parameter
    ''' Could be improved'''
    unified_field_mappings = requested_social_media_data[0]['endpoint_mapping'][endpoint]
    test_for_none = unified_field_mappings['endpoint']
    if path != None:
        unified_field_mappings = unified_field_mappings['paths'][path]
        test_for_none = unified_field_mappings['path']
    
    print
    # If no fields are selected, return all possible data
    if test_for_none != None and fields == None:
        unified_fields = unified_field_mappings[type_of_fields].keys()
    
    # Map fields for similar parameter for each platform
    for social_media in requested_social_media_data:

        # set location of field mappings depending on presence of path parameter
        field_mappings = social_media['endpoint_mapping'][endpoint]

        if path != None:
            field_mappings = field_mappings['paths'][path]

        # skip social media if endpoint does not exist for it
        if test_for_none == None:
            mapped_fields = None
            continue

        # Map for GET method
        if method == 'get':
            temp_fields = []

            if fields == None:
                # Collate all possible fields
                for field in field_mappings[type_of_fields]:
                    if field_mappings[type_of_fields][field] != None:
                        temp_fields.append(field_mappings[type_of_fields][field])
                
            else:
                # Collate requested fields
                for field in unified_fields:
                    if field not in field_mappings[type_of_fields]:
                        error = {
                            'Error': {
                                'HTTPstatus': 400,
                                'error_code': 4,
                                'message': f'Field {field} is not a valid field. See data dictionaries for all available fields.'
                            }
                        }
                        raise HTTPException(status_code=400, detail=error)

                    if field_mappings[type_of_fields][field] != None:
                        temp_fields.append(field_mappings[type_of_fields][field])
                
            # Add mapped fields to the list
            mapped_fields[social_media['name']] = temp_fields

        # Map for POST method
        elif method == 'post':
            temp_fields = {}
            for field in unified_fields:
                if field_mappings[type_of_fields][field] != None:
                    try:
                        temp_fields[field_mappings[type_of_fields][field]] = json.loads(fields[field])
                    except:
                        temp_fields[field_mappings[type_of_fields][field]] = fields[field]
            
            # Add mapped fields to the list
            mapped_fields[social_media['name']] = temp_fields

    return unified_fields, mapped_fields


def prepare_endpoint_error_response(sm_platform, url):
    error = {
        'Error': {
            'HTTPstatus': 400,
            'error_code': 6,
            'message': f'Endpoint: {url} is not supported for {sm_platform}.'
        }
    }
    response = Response()
    response.status_code = 400
    response.reason = error
    response.json = error
    return response

def call_social_media_APIs(method, requested_social_media, endpoint, path=None, id=None, fields=None, limit=None):
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
    try:
        unified_fields, mapped_fields = map_fields(method, requested_social_media, endpoint, path, fields)
    except HTTPException as e:
        response = Response()
        response.status_code = e.status_code
        response.reason = e.detail
        response.json = e.detail
        return response
    
    url = '/' + endpoint
    if id != None:
        url += '/' + id
    if path != None:
        url += '/' + path

    if mapped_fields == None:
        error = {
            'Error': {
                'HTTPstatus': 400,
                'error_code': 5,
                'message': f'None of the selected social media APIs are supported for the endpoint: {url}.'
            }
        }
        response = Response()
        response.status_code = 400
        response.reason = error
        response.json = error
        return response

    # call social media APIs
    if 'fb' in requested_social_media:
        if 'Facebook' not in mapped_fields:
            responses['fb'] = prepare_endpoint_error_response('Facebook', url)
        else:
            responses['fb'] = call_fb_api(fb_access, data_dictionary['fb'], method, endpoint, path, mapped_fields[data_dictionary['fb']['name']], id)
    
    if 'ig' in requested_social_media:
        if 'Instagram' not in mapped_fields:
            responses['ig'] = prepare_endpoint_error_response('Instagram', url)
        else:
            responses['ig'] = call_ig_api(ig_access, data_dictionary['ig'], method, endpoint, path, mapped_fields[data_dictionary['ig']['name']], id)
    
    if 'ln' in requested_social_media:
        if 'LinkedIn' not in mapped_fields:
            responses['ln'] = prepare_endpoint_error_response('LinkedIn', url)
        else:
            responses['ln'] = call_ln_api(ln_access, data_dictionary['ln'], method, endpoint, path, mapped_fields[data_dictionary['ln']['name']], id)

    if 'tw' in requested_social_media:
        if 'Twitter' not in mapped_fields:
            responses['tw'] = prepare_endpoint_error_response('Twitter', url)
        else:
            responses['tw'] = call_tw_api(tw_api, data_dictionary['tw'], method, endpoint, path, mapped_fields[data_dictionary['tw']['name']], id)

    # merge responses into one json object
    response = merge_responses(method, endpoint, unified_fields, responses, limit)
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


def call_social_media_APIs_with_id(method, sm, endpoint, path, id, fields=None, limit=None):
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

    response = call_social_media_APIs(method, requested_social_media, endpoint, path, id=id, fields=fields, limit=limit)
    return response



# https://127.0.0.1:443/users/{user_id}/posts?sm=ln&author=cAnJ0yFHOX&state=PUBLISHED&visible_to_ln=CONNECTIONS&content={"shareCommentary":"Testni tekst","shareMediaCategory":"NONE"}
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

@app.get('/ig_auth')
def get_ig_code(code: str, error_reason: str=None, error_description: str=None):
    try:
        global ig_access
        ig_access = ig_auth_2(code, file_with_ig_credentials).json()['access_token']
        ig_authenticated = True
        response = 'Success'
    except:
        response = 'Error'
        if error_reason and error_description:
            response = 'Error: ' + error_reason + ', ' + error_description
    
    return response

@app.get('/ln_auth')
def get_ln_code(code: str):
    try:
        global ln_access
        ln_access = ln_auth_2(code, file_with_ln_credentials)
        ln_authenticated = True
        response = 'Success'
    except:
        response = 'Error'
    return response

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
            ig_auth(file_with_ig_credentials)
        except:
            response['Instagram'] = 'Error'
    
    if 'ln' in requested_social_media:
        try:
            ln_auth(file_with_ln_credentials)
        except:
            response['LinkedIn'] = 'Error'

    if 'tw' in requested_social_media:
        tw_creds, tw_error = tw_auth(file_with_tw_credentials)
        if tw_error != None:
            global tw_access
            tw_access = tw_creds
            response['Twitter'] = tw_error
        tw_authenticated = True
        response['Twitter'] = 'Success'

    return response

# @app.get('/ig_deauth')
# @app.get('/ig_delete_data')

##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################

# fb, ig
# Facebook: fields, permissions and error codes: https://developers.facebook.com/docs/graph-api/reference/album
@app.get('/albums/{album_id}')
def get_data_abut_album(album_id: str, sm: str, fields: str = None, limit: str = None):
    '''Returns data about the album with given album_id specified by parameter `fields`'''

    endpoint = 'albums'
    method = 'get'
    response = call_social_media_APIs_with_id(method, sm, endpoint, None, album_id, fields=fields, limit=limit)
    return response


# fb
# Facebook: Access to Events on Users and Pages is only available to Facebook Marketing Partners.
@app.get('/events/{event_id}')
def get_data_about_event(event_id: str, sm: str, fields: str = None, limit: str = None):
    '''Returns data about the event with given event_id specified by parameter `fields`'''

    endpoint = 'events'
    method = 'get'
    response = call_social_media_APIs_with_id(method, sm, endpoint, None, event_id, fields=fields, limit=limit)
    return response


# fb: Fields that return User information will not be included in any responses unless the request is made using an access token of an Admin of the Group.
@app.get('/groups/{group_id}')
def get_data_about_group(group_id: str, sm: str, fields: str = None, limit: str = None):
    '''Returns data about the group with given group_id specified by parameter `fields`'''

    endpoint = 'groups'
    method = 'get'
    response = call_social_media_APIs_with_id(method, sm, endpoint, None, group_id, fields=fields, limit=limit)
    return response


# fb
@app.get('/links/{link_id}')
def get_data_about_link(link_id: str, sm: str, fields: str = None, limit: str = None):
    '''Returns data about the link with given link_id specified by parameter `fields`'''

    endpoint = 'links'
    method = 'get'
    response = call_social_media_APIs_with_id(method, sm, endpoint, None, groulink_idp_id, fields=fields, limit=limit)
    return response
# TO BE TESTED


# fb
@app.get('/live_videos/{video_id}')
def get_data_about_live_video(video_id: str, sm: str, fields: str = None, limit: str = None):
    '''Returns data about the live video with given video_id specified by parameter `fields`'''

    endpoint = 'live_videos'
    method = 'get'
    response = call_social_media_APIs_with_id(method, sm, endpoint, None, video_id, fields=fields, limit=limit)
    return response


# fb, ln, tw
@app.get('/me')
def get_data_about_me(sm: str, fields: str = None, limit: str = None):
    '''Returns data about the logged-in user specified by parameter `fields`'''

    endpoint = 'me'
    method = 'get'
    requested_social_media = sm.split(',') # Because this endpoint is not id dependent
    response = call_social_media_APIs(method, requested_social_media, endpoint, None, fields=fields, limit=limit)
    return response
    

# fb, ig
@app.get('/photos/{photo_id}')
def get_data_about_photo(photo_id: str, sm: str, fields: str = None, limit: str = None):
    '''Returns data about the photo with given photo_id specified by parameter `fields`'''

    endpoint = 'photos'
    method = 'get'
    response = call_social_media_APIs_with_id(method, sm, endpoint, None, photo_id, fields=fields, limit=limit)
    return response


# fb
@app.get('/posts/{post_id}')
def get_data_about_post(post_id: str, sm: str, fields: str = None, limit: str = None):
    '''Returns data about the post with given post_id specified by parameter `fields`'''

    endpoint = 'posts'
    method = 'get'
    response = call_social_media_APIs_with_id(method, sm, endpoint, None, post_id, fields=fields, limit=limit)
    return response


# TO BE TESTED
# fb, ig
@app.get('/users/{user_id}')
def get_data_about_user(user_id: str, sm: str, fields: str = None, limit: str = None):
    '''Returns data about the user with given user_id specified by parameter `fields`'''

    endpoint = 'users'
    method = 'get'
    response = call_social_media_APIs_with_id(method, sm, endpoint, None, user_id, fields=fields, limit=limit)
    return response


# fb, ig
@app.get('/videos/{video_id}')
def get_data_about_video(video_id: str, sm: str, fields: str = None, limit: str = None):
    '''Returns data about the video with given video_id specified by parameter `fields`'''

    endpoint = 'videos'
    method = 'get'
    response = call_social_media_APIs_with_id(method, sm, endpoint, None, video_id, fields=fields, limit=limit)
    return response


# POST requests

# TO BE TESTED
# fb
@app.post('/albums/{album_id}/photos')
def create_photo_in_album(
    album_id: str, 
    sm: str,
    allow_spherical_photo: bool=False,
    alt_text: str=None,
    android_key_hash: str=None,
    itunes_app_id: str=None,
    attempt: int=0,
    is_audience_experience: bool=False,
    dated: str=None,
    dated_accuracy: str=None,
    description: str=None,
    composer_session_id: str=None,
    sponsor_boost_status: int=None,
    feed_targeting: str=None,
    full_res_is_coming_later: bool=False,
    override_initial_view_heading_degrees: int=None,
    override_initial_view_pitch_degrees: int=None,
    override_initial_view_vertical_fov_degrees: int=None,
    ios_bundle_id: str=None,
    is_explicit_location: bool=None,
    is_place_tag: bool=None,
    is_visual_search: bool=None,
    manual_privacy: bool=False,
    no_story: bool=None,
    offline_id: int=0,
    open_graph_action_type_id: str=None,
    open_graph_icon_id: str=None, 
    open_graph_object_id: str=None,
    open_graph_phrase: str=None,
    open_graph_set_profile_badge: bool=False,
    open_graph_suggestion_mechanism: str=None,
    location_by_id: str=None,
    visible_to_fb: str=None,
    proxied_app_id: str=None,
    is_published: bool=True,
    photos_waterfall_id: str=None,
    scheduled_publish_time: int=None,
    spherical_metadata: str=None,
    sponsor_id: str=None,
    sponsor_relationship: str=None,
    tagged_users: list=None,
    targeting: str=None,
    timedelta_since_dated: int=None,
    unpublished_content_type: str=None,
    source_url_of_photo: str=None,
    user_selected_tags: bool=False,
    vault_image_id: str=None
    ):
    '''Creates a photo in album with given album_id.'''

    fields = locals().copy()

    endpoint = 'albums'
    path = 'photos'
    method = 'post'

    del fields['album_id']
    del fields['sm']

    response = call_social_media_APIs_with_id(method, sm, endpoint, path, album_id, fields=fields)
    return response


# TO BE TESTED
# fb
@app.post('/events/{event_id}/live_videos')
def create_live_video_in_event(
    event_id: str, 
    sm: str, 
    app_id: str=None, 
    content_tags: list=None, 
    description: str=None, 
    enable_backup_ingest: bool=False, 
    encoding_settings_identifier: str=None, 
    fisheye_video_cropped: bool=None, 
    front_z_rotation: float=None, 
    is_360: bool=False, 
    live_encoders: list=None, 
    original_fov: int=None,
    visible_to_fb: str=None,
    projection: str='eqirectangular',
    custom_image_for_schedule: str=None,
    spatial_audio_format: int=None,
    status: str='unpublished',
    stereoscopic_mode: str='mono',
    stop_on_delete_stream: bool=False,
    video_title: str=Query(None, max_length=254)
    ):
    '''Creates a live video in event with given event_id.'''

    fields = locals().copy()

    endpoint = 'events'
    path = 'live_videos'
    method = 'post'

    del fields['event_id']
    del fields['sm']

    response = call_social_media_APIs_with_id(method, sm, endpoint, path, event_id, fields=fields)
    return response


# fb: fields:https://developers.facebook.com/docs/graph-api/reference/album
@app.post('/groups/{group_id}/albums')
def create_album_in_group(group_id:str, sm:str, name: str, description: str=None, visible_to_fb: str=None, make_shared_album: bool=False, contributors: list=None, location_by_id: str=None, location_by_name: str=None):
    ''' Creates a new album in a group specified by group_id '''

    fields = locals().copy()

    endpoint = 'groups'
    path = 'albums'
    method = 'post'

    del fields['group_id']
    del fields['sm']

    response = call_social_media_APIs_with_id(method, sm, endpoint, path, group_id, fields=fields)
    return response


# TO BE TESTED
# video_title: str=Query('None', max_length=254)
# fb
@app.post('/groups/{group_id}/live_videos')
def create_live_video_in_group(
    group_id: str, 
    sm: str, 
    app_id: str=None,
    app_tag: str=None, 
    content_tags: list=None, 
    description: str=None,
    dont_show_on: list=None, 
    enable_backup_ingest: bool=False, 
    encoding_settings_identifier: str=None, 
    fisheye_video_cropped: bool=None, 
    front_z_rotation: float=None, 
    game_id: str=None,
    game_specs: str=None,
    is_360: bool=False, 
    live_encoders: list=None, 
    original_fov: int=None,
    visible_to_fb: str=None,
    projection: str='eqirectangular',
    custom_image_for_schedule: str=None,
    save_vod: bool=True,
    spatial_audio_format: int=None,
    status: str='unpublished',
    stereoscopic_mode: str='mono',
    stop_on_delete_stream: bool=False,
    video_title: str=None
    ):
    '''Creates a live video in group with given group_id.'''

    fields = locals().copy()

    endpoint = 'groups'
    path = 'live_videos'
    method = 'post'

    del fields['group_id']
    del fields['sm']

    response = call_social_media_APIs_with_id(method, sm, endpoint, path, group_id, fields=fields)
    return response


# TO BE TESTED
# fb
@app.post('/groups/{group_id}/photos')
def create_photo_in_group(
    group_id: str, 
    sm: str,
    allow_spherical_photo: bool=False,
    alt_text: str=None,
    android_key_hash: str=None,
    itunes_app_id: str=None,
    attempt: int=0,
    is_audience_experience: bool=False,
    dated: str=None,
    dated_accuracy: str=None,
    description: str=None,
    composer_session_id: str=None,
    sponsor_boost_status: int=None,
    feed_targeting: str=None,
    full_res_is_coming_later: bool=False,
    override_initial_view_heading_degrees: int=None,
    override_initial_view_pitch_degrees: int=None,
    override_initial_view_vertical_fov_degrees: int=None,
    ios_bundle_id: str=None,
    is_explicit_location: bool=None,
    is_place_tag: bool=None,
    is_visual_search: bool=None,
    manual_privacy: bool=False,
    no_story: bool=None,
    offline_id: int=0,
    open_graph_action_type_id: str=None,
    open_graph_icon_id: str=None, 
    open_graph_object_id: str=None,
    open_graph_phrase: str=None,
    open_graph_set_profile_badge: bool=False,
    open_graph_suggestion_mechanism: str=None,
    location_by_id: str=None,
    visible_to_fb: str=None,
    proxied_app_id: str=None,
    is_published: bool=True,
    photos_waterfall_id: str=None,
    scheduled_publish_time: int=None,
    spherical_metadata: str=None,
    sponsor_id: str=None,
    sponsor_relationship: str=None,
    tagged_users: list=None,
    targeting: str=None,
    timedelta_since_dated: int=None,
    unpublished_content_type: str=None,
    source_url_of_photo: str=None,
    user_selected_tags: bool=False,
    vault_image_id: str=None
    ):
    '''Creates a photo in group with given group_id.'''

    fields = locals().copy()

    endpoint = 'groups'
    path = 'photos'
    method = 'post'

    del fields['group_id']
    del fields['sm']

    response = call_social_media_APIs_with_id(method, sm, endpoint, path, group_id, fields=fields)
    return response


# fb
@app.post('/groups/{group_id}/posts')
def create_post_in_group(
    group_id: str, 
    sm: str,
    message: str=None,
    link: str=None
    ):
    '''Creates a post in group with given group_id.'''

    fields = locals().copy()

    endpoint = 'groups'
    path = 'posts'
    method = 'post'

    del fields['group_id']
    del fields['sm']

    response = call_social_media_APIs_with_id(method, sm, endpoint, path, group_id, fields=fields)
    return response

# TO BE TESTED
# fb
@app.post('/groups/{group_id}/videos')
def create_video_in_group(
    group_id: str, 
    sm: str, 
    video_encoded_as_form_data: str,
    video_file_chunk: str,
    audio_story_wave_animation_handle: str=None,
    content_category: str=None,
    description: str=None,
    embeddable: bool=None,
    end_offset: int=None,
    file_size_in_bytes: int=None,
    file_url: str=None,
    fisheye_video_cropped: bool=None,
    vertical_fov_for_360: int=None,
    front_z_rotation: float=None,
    guide_keyframes_data_for_360: list=None,
    guide_enabled_for_360: bool=None,
    initial_heading_for_360: int=None,
    initial_pitch_for_360: int=None,
    original_fov: int=None,
    original_projection_type_for_360: str='eqirectangular',
    prompt_id: str=None,
    prompt_tracking_string: str=None,
    react_mode_metadata: str=None,
    referenced_sticker_id: str=None,
    video_id_to_replace: str=None,
    scheduled_publish_time: int=None,
    slideshow_spec: str=None,
    source_instagram_media_id: str=None,
    is_360: bool=False,
    start_offset: int=None,
    swap_mode: str=None,
    video_title: str=None,
    transcode_setting_properties: str=None,
    unpublished_content_type: str=None,
    upload_phase: str=None,
    upload_session_id: str=None,
    ):
    '''Creates a video in group with given group_id.'''

    fields = locals().copy()

    endpoint = 'groups'
    path = 'videos'
    method = 'post'

    del fields['group_id']
    del fields['sm']

    response = call_social_media_APIs_with_id(method, sm, endpoint, path, group_id, fields=fields)
    return response

# TO BE TESTED
# Not sure if fields are ok, since two documentation pages about this have different fields listed. To be tested.
# fb
@app.post('/live_videos/{video_id}')
def update_live_video(
    video_id: str, 
    sm: str, 
    allow_bm_crossposting: bool=None,
    content_tags: list=None, 
    crossposting_actions: list=None,
    cross_share_to_group_ids: list=None,
    custom_labels: list=None,
    description: str=None, 
    sponsor_boost_status: int=None,
    is_disturbing: bool=None,
    donate_button_charity_id: str=None, 
    embeddable: bool=None,
    end_live_video: bool=None,
    is_manual_mode: bool=None,
    live_comment_moderation_setting: list=None,
    live_encoders: list=None, 
    master_ingest_stream_id: str=None,
    location: str=None,
    planned_start_time: int=None,
    visible_to_fb: str=None,
    projection: str='eqirectangular',
    custom_image_for_schedule: str=None,
    custom_background_image_for_schedule: str=None,
    persistent_stream_key_status: str=None,
    sponsor_id: str=None,
    sponsor_relationship: int=None,
    status: str='unpublished',
    tagged_users: list=None,
    targeting: str=None,
    video_title: str=Query(None, max_length=254)
    ):
    '''Updates a live video with given video_id.'''

    fields = locals().copy()

    endpoint = 'live_videos'
    method = 'post'

    del fields['video_id']
    del fields['sm']

    response = call_social_media_APIs_with_id(method, sm, endpoint, None, video_id, fields=fields)
    return response


# fb
@app.post('/users/{user_id}')
def update_user_profile(
    user_id: str, 
    sm: str, 
    dismiss_local_news_megaphone: bool=None,
    emoji_color_pref: int=None,
    first_name: str=None,
    last_name: str=None,
    set_local_news_notifications: bool=None
    ):
    '''Updates a user profile with given user_id.'''

    fields = locals().copy()

    endpoint = 'users'
    method = 'post'

    del fields['user_id']
    del fields['sm']

    response = call_social_media_APIs_with_id(method, sm, endpoint, None, user_id, fields=fields)
    return response

# TO BE TESTED
# fb
@app.post('/users/{user_id}/live_videos')
def create_live_video_on_user(
    user_id: str, 
    sm: str, 
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
    visible_to_fb: str=None,
    projection: str='eqirectangular',
    custom_image_for_schedule: str=None,
    spatial_audio_format: int=None,
    status: str='unpublished',
    stereoscopic_mode: str='mono',
    stop_on_delete_stream: bool=False,
    video_title: str=Query(None, max_length=254)
    ):
    '''Creates a live video on users profile with given user_id.'''

    fields = locals().copy()

    endpoint = 'users'
    path = 'live_videos'
    method = 'post'

    del fields['user_id']
    del fields['sm']

    response = call_social_media_APIs_with_id(method, sm, endpoint, path, user_id, fields=fields)
    return response


# ln
@app.post('/users/{user_id}/posts')
def create_post_on_user(
    user_id: str, 
    sm: str,
    author: str,
    content: str,
    state: str,
    visible_to_ln: str
    ):
    '''Creates a post on users profile with given user_id.'''

    fields = locals().copy()

    endpoint = 'users'
    path = 'posts'
    method = 'post'

    del fields['user_id']
    del fields['sm']

    response = call_social_media_APIs_with_id(method, sm, endpoint, path, user_id, fields=fields)
    return response

# TO BE TESTED
# fb
@app.post('/users/{user_id}/videos')
def create_video_on_user(
    user_id: str, 
    sm: str, 
    video_encoded_as_form_data: str,
    video_file_chunk: str,
    audio_story_wave_animation_handle: str=None,
    content_category: str=None,
    description: str=None,
    sponsor_boost_status: int=None,
    embeddable: bool=None,
    end_offset: int=None,
    file_size_in_bytes: int=None,
    file_url: str=None,
    fisheye_video_cropped: bool=None,
    vertical_fov_for_360: int=None,
    front_z_rotation: float=None,
    guide_keyframes_data_for_360: list=None,
    guide_enabled_for_360: bool=None,
    initial_heading_for_360: int=None,
    initial_pitch_for_360: int=None,
    is_voice_clip: bool=None,
    no_story: bool=False,
    original_fov: int=None,
    original_projection_type_for_360: str='eqirectangular',
    posting_to_redspace: bool=None,
    visible_to_fb: str=None,
    prompt_id: str=None,
    prompt_tracking_string: str=None,
    react_mode_metadata: str=None,
    referenced_sticker_id: str=None,
    video_id_to_replace: str=None,
    slideshow_spec: str=None,
    source_instagram_media_id: str=None,
    is_360: bool=False,
    sponsor_id: str=None,
    start_offset: int=None,
    swap_mode: str=None,
    video_title: str=None,
    transcode_setting_properties: str=None,
    unpublished_content_type: str=None,
    upload_phase: str=None,
    upload_session_id: str=None,
    video_id_original: str=None
    ):
    '''Creates a video on users profile with given user_id.'''

    fields = locals().copy()

    endpoint = 'users'
    path = 'videos'
    method = 'post'

    del fields['user_id']
    del fields['sm']

    response = call_social_media_APIs_with_id(method, sm, endpoint, path, user_id, fields=fields)
    return response

# TO BE TESTED
# fb
@app.post('/videos/{video_id}')
def update_video(
    user_id: str, 
    sm: str, 
    ad_breaks: list=None,
    allow_bm_crossposting: bool=None,
    allow_crossposting_for_pages: list=None,
    dated: str=None,
    dated_accuracy: str=None,
    call_to_action: str=None,
    content_category: str=None,
    content_tags: list=None,
    custom_labels: list=None,
    description: str=None,
    sponsor_boost_status: int=None,
    embeddable: bool=None,
    expiration: str=None,
    expire_now: bool=None,
    increment_play_count: bool=None,
    video_title: str=None,
    preferred_thumbnail_id: str=None,
    visible_to_fb: str=None,
    publish_to_news_feed: bool=None,
    publish_to_videos_tab_only: bool=None,
    is_published: bool=None,
    scheduled_publish_time: int=None,
    social_actions_disabled: bool=None,
    sponsor_id: str=None,
    sponsor_relationship: str=None,
    tagged_users: list=None,
    target_video_id: str=None,
    universal_video_id: str=None
    ):
    '''Updates a video with given video_id.'''

    fields = locals().copy()

    endpoint = 'videos'
    method = 'post'

    del fields['video_id']
    del fields['sm']

    response = call_social_media_APIs_with_id(method, sm, endpoint, None, video_id, fields=fields)
    return response



# DELETE requests

# TO BE TESTED
#fb
@app.delete('/live_videos/{video_id}')
def delete_live_video(video_id: str, sm: str):
    '''Delete a live video with given video_id'''

    endpoint = 'live_video'
    method = 'delete'

    response = call_social_media_APIs_with_id(method, sm, endpoint, None, video_id)
    return response


# TO BE TESTED
#fb
@app.delete('/photos/{photo_id}')
def delete_photo(photo_id: str, sm: str):
    '''Delete a photo with given photo_id'''

    endpoint = 'photos'
    method = 'delete'

    response = call_social_media_APIs_with_id(method, sm, endpoint, None, photo_id)
    return response


# TO BE TESTED
#fb
@app.delete('/videos/{video_id}')
def delete_video(video_id: str, sm: str):
    '''Delete a video with given video_id'''

    endpoint = 'videos'
    method = 'delete'

    response = call_social_media_APIs_with_id(method, sm, endpoint, None, video_id)
    return response


# TODO: Add LinkedIn endpoints and mappings
# TODO: Add Twitter endpoints and mappings
# TODO: Add mapping of the privacy values https://developers.facebook.com/docs/graph-api/reference/privacy/
# Example use

# POST parameters in body? Yes, if we implement Models, otherwise they are expected as query parameters. See https://fastapi.tiangolo.com/tutorial/body/
'''
The function parameters will be recognized as follows:

- If the parameter is also declared in the path, it will be used as a path parameter.
- If the parameter is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query parameter.
- If the parameter is declared to be of the type of a Pydantic model, it will be interpreted as a request body.
'''

# Limit default value
# Apply limit while paging

# Error handling for nonexistent paths (it's fine, there is no interval server error but still, error message doens't tell you much)


# TODO: create method for authentication that checks validity of all credentials, maybe /authenticate and/or /authenticate/sm_name
# TODO: twitter authentication (maybe even offer login with bearer token in addition to user login)
# TODO: fb authentication
# TODO: For the fb app to make it usable to non-authors, we need to implement Facebook Data Deletion Callback: https://developers.facebook.com/docs/development/build-and-test
# TODO: Refresh Facebook user access token (otherwise it my expire in 2 hours)
# data deletion for fb and ig
# deauth for ig

# FURTHER DEVELOPMENT: Put instead of Post for updating stuff
# FURTHER DEVELOPMENT: Also now all of the data has to be saved in files, maybe it would be better to make it so that all the neccessary data is passed via call to /auth.
# FURTHER DEVELOPMENT: If too much time, implement parameter "group_by" that allows you to either group by data first or by provider first.
# FURTHER DEVELOPMENT: When you query, the app checks if all permissions are avaliable and if not it asks you for the permission - aka prompts login and creates access token
# FURTHER DEVELOPMENT: Beginning with SDK v13.0 for iOS and Android, set to release in early 2022, a Client Token will be required for all calls to the Graph API. https://developers.facebook.com/docs/facebook-login/access-tokens/
# FURTHER DEVELOPMENT: Add suggestions on how to resolve the error in the merged response. Either from the docs of social media APIs or from us if it's something with this api.
# FURTHER DEVELOPMENT: expansion/multiple requests in one https://developers.facebook.com/docs/graph-api/field-expansion/
# FURTHER DEVELOPMENT: Add Facebook's edges also as endpoints, not just as fields
# FURTHER DEVELOPMENT: Create data dictionaries on the go from csv tables for each endpoint (easier to update/add/remove an endpoint or field)
# FURTHER DEVELOPMENT: fields=all-sth Make it possible to instead of specifying all e.g. 33 fields out of 35, we just say all but not this and that.
# FURTHER DEVELOPMENT: If no fields are provided in get request, use not all of them but all that are non None value for requested sm.
# FURTHER DEVELOPMENT: Add this type (fb): /search?type=adinterest&q=TEDx


# QUICK TEST
# print(authenticate('fb,ig,ln'))
# print(get_data_about_me(sm='ig,ln'))
# ,fields='id,first_name,last_name,birthday'

# print(get_data_about_group(group_id='2998732937039201', sm='fb'))
# print(create_album_in_group(group_id= '2998732937039201', sm='fb', name='My first album', description='Testing for spaces'))
# print(get_data_abut_album(album_id='379274703677170', sm='fb'))
# print(get_data_about_user('10215963448399509', 'fb', 'name,id,birthday'))
# print(get_data_about_event(event_id='845071692823639', sm='fb'))

# print(comment_on_album(album_id='379274703677170', sm='fb', message='Testni komentar')) # WARNING: does not work with user access token for fb
# print(reply_to_comment(comment_id='3000284600217368', sm='fb', message='Testni komentar')) # WARNING: does not work with user access token for fb
# print(get_data_about_comment(comment_id='3000284600217368', sm='fb')) # WARNING: does not work with user access token for fb

# group 2998732937039201
# album 1952607818239826
# album with 1 photo and 1 comment: 379274703677170
# comment on album in a group: 3000284600217368
# event in group: 845071692823639

asyncio.run(serve(app, hypercorn_config))


# https://127.0.0.1:443/groups/2998732937039201/albums?sm=fb&name=Test&description=Nanana
# param contributors must be an array

# https://127.0.0.1:443/users/cAnJ0yFHOX/posts?sm=ln&author=cAnJ0yFHOX&state=PUBLISHED&visible_to_ln=CONNECTIONS&content={"shareCommentary":"Testni tekst","shareMediaCategory":"NONE"}