import json
from pyfacebook import GraphAPI
import webbrowser
import requests
from .utility import Utility as ut


def auth(file_with_credentials):
    credentials = ut.read_credentials(file_with_credentials)
    app_token, app_secret, redirect_uri, app_display_name = credentials['fb_app_token'], credentials['fb_app_secret'], credentials['redirect_uri'], credentials['app_display_name']

    api_url = "https://www.facebook.com/dialog/oauth"
    params = {
        'response_type':'code',
        'client_id': app_token,
        'redirect_uri': redirect_uri,
        'scope': 'public_profile,user_birthday,user_hometown,user_location,user_likes,user_events,user_photos,user_videos,user_friends,user_posts,user_gender,user_link,user_age_range,email,read_insights,publish_video,gaming_user_locale,user_managed_groups,groups_show_list,pages_show_list,ads_management,ads_read,publish_to_groups,groups_access_member_info,leads_retrieval,attribution_read,page_events,pages_read_engagement,pages_read_user_content',
        'state': app_display_name
    }

    response = requests.get(f'{api_url}',params=params)
    webbrowser.open(response.url)


def auth_part_2(code, file_with_credentials):
    credentials = ut.read_credentials(file_with_credentials)
    app_token, app_secret, redirect_uri, app_display_name = credentials['fb_app_token'], credentials['fb_app_secret'], credentials['redirect_uri'], credentials['app_display_name']

    api_url = 'https://graph.facebook.com/v12.0/oauth/access_token'
    params = {
        'client_id': app_token,
        'client_secret': app_secret,
        'redirect_uri': redirect_uri + '/',
        'code': code
    }
    response = requests.get(f'{api_url}', params=params)
    return response.json()['access_token']
