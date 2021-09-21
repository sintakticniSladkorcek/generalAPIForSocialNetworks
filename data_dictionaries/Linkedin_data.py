class Linkedin_data():
    dict = {
        'name': 'Linkedin',
        'base_url': 'https://api.linkedin.com/v2/',
        'endpoint_mapping': {
            'albums': {
                'endpoint': None
            },
            'events': {
                'endpoint': None
            },
            'groups': {
                'endpoint': None
            },
            'links': {
                'endpoint': None
            },
            'live_video': {
                'endpoint': None
            },
            'me': {
                'endpoint': 'me',
                'get_fields': {
                    'account_type': None,
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
                    'liked_pages': None,
                    'link': None,
                    'live_encoders': None,
                    'live_videos': None,
                    'location': None,
                    'media_count': None,
                    'meeting_for': None,
                    'middle_name': None,
                    'music': None,
                    'name':'firstName,lastName', # collate first and last name
                    'name_format': None,
                    'pages_with_roles': None,
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
                    'username': None,
                    'video_upload_limits': None,
                    'videos': None
                }
            },
            'photos': {
                'endpoint': None
            },
            'posts': {
                'endpoint': None
            },
            'users': {
                'endpoint': None
            },
            'videos': {
                'endpoint': None
            }
        }
    }