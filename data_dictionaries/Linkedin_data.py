class Linkedin_data():
    dict = {
        'name': 'Linkedin',
        'base_url': 'https://api.linkedin.com/v2/',
        'endpoint_mapping': {
            'album': {
                'endpoint': None
            },
            'comment': {
                'endpoint': None
            },
            'event': {
                'endpoint': None
            },
            'group': {
                'endpoint': None
            },
            'live_video': {
                'endpoint': None
            },
            'me': {
                'endpoint': 'me',
                'get_fields': {
                    'accounts': None,
                    'ad_studies': None,
                    'adaccounts': None,
                    'age_range': None,
                    'albums': None,
                    'apprequestformerrecipients': None,
                    'apprequests': None,
                    'assigned_business_asset_groups': None,
                    'birthday': None,
                    'business_users': None,
                    'businesses': None,
                    'email': None,
                    'events': None,
                    'first_name_by_location': 'firstName',
                    'favorite_athletes': None,
                    'favorite_teams': None,
                    'feed': None,
                    'first_name':'localizedFirstName',
                    'connections': None,
                    'gender': None,
                    'groups': None,
                    'hometown': None,
                    'id':'id',
                    'inspirational_people': None,
                    'install_type': None,
                    'installed': None,
                    'is_guest_user': None,
                    'languages': None,
                    'last_name':'localizedLastName',
                    'last_name_by_location': 'lastName',
                    'likes': None,
                    'link': None,
                    'live_encoders': None,
                    'live_videos': None,
                    'location': None,
                    'meeting_for': None,
                    'middle_name': None,
                    'music': None,
                    'name':'firstName',
                    'name_format': None,
                    'payment_pricepoints': None,
                    'permissions': None,
                    'personal_ad_accounts': None,
                    'photos': None,
                    'profile_picture': None,
                    'posts': None,
                    'quotes': None,
                    'rich_media_documents': None,
                    'shared_login_upgrade_required_by': None,
                    'short_name': None,
                    'significant_other': None,
                    'sports': None,
                    'supports_donate_button_in_live_video': None,
                    'video_upload_limits': None,
                    'videos': None
                }
            },
            'page': {
                'endpoint': None
            },
            'post': {
                'endpoint': None
            },
            'user': {
                'endpoint': None
            }
        }
    }