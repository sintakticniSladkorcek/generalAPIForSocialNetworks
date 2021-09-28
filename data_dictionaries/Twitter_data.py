class Twitter_data():
    dict = {
        'name': 'Twitter',
        'base_url': 'https://api.twitter.com/2/',
        'endpoint_mapping': {
            'albums': {
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
                    'account_type': None,
                    'accounts': None,
                    'ad_studies': None,
                    'age_range': None,
                    'albums': None,
                    'apprequestformerrecipients': None,
                    'apprequests': None,
                    'assigned_business_asset_groups': None,
                    'birthday': None,
                    'business_users': None,
                    'businesses': None,
                    'connections': None,
                    'created_at': 'created_at',
                    'description': 'description',
                    'email': None,
                    'events': None,
                    'first_name_by_location': None,
                    'favorite_athletes': None,
                    'favorite_teams': None,
                    'feed': None,
                    'first_name': None,
                    'gender': None,
                    'groups': None,
                    'hometown': None,
                    'id':'id',
                    'inspirational_people': None,
                    'install_type': None,
                    'installed': None,
                    'is_guest_user': None,
                    'is_private': 'protected',
                    'languages': None,
                    'last_name': None,
                    'last_name_by_location': None,
                    'liked_pages': None,
                    'link': None,
                    'live_encoders': None,
                    'live_videos': None,
                    'location': 'location',
                    'media_count': None,
                    'meeting_for': None,
                    'metrics': 'public_metrics',
                    'middle_name': None,
                    'music': None,
                    'name': 'name',
                    'name_format': None,
                    'pages_with_roles': None,
                    'payment_pricepoints': None,
                    'permissions': None,
                    'photos': None,
                    'profile_picture': 'profile_image_url',
                    'posts': None,
                    'quotes': None,
                    'rich_media_documents': None,
                    'shared_login_upgrade_required_by': None,
                    'short_name': None,
                    'significant_other': None,
                    'sports': None,
                    'supports_donate_button_in_live_video': None,
                    'url': 'url',
                    'username': 'username',
                    'verified': 'verified',
                    'video_upload_limits': None,
                    'videos': None
                }
            },
            'photos': {
                'endpoint': None
            },
            'posts': {
                'endpoint': 'get_status()'
            },
            'users': {
                'endpoint': 'users',
                'get_fields': {
                    'account_type': None,
                    'ad_studies': None,
                    'age_range': None,
                    'albums': None,
                    'apprequests': None,
                    'assigned_business_asset_groups': None,
                    'assigned_pages': None,
                    'assigned_product_catalogs': None,
                    'birthday': None,
                    'business_users': None,
                    'businesses': None,
                    'conversations': None,
                    'created_at': 'created_at', # The UTC datetime that the user account was created on Twitter. "created_at": "2013-12-14T04:35:55.000Z"
                    'custom_labels': None,
                    'description': 'description', # The text of this user's profile description (also known as bio), if the user provided one.
                    'email': None,
                    'favorite_athletes': None,
                    'favorite_teams': None,
                    'feed': None,
                    'first_name': None,
                    'friends': None,
                    'gender': None,
                    'hometown': None,
                    'id': 'id', # The unique identifier of this user.
                    'ids_for_apps': None,
                    'ids_for_business': None,
                    'ids_for_pages': None,
                    'inspirational_people': None,
                    'install_type': None,
                    'is_installed': None,
                    'is_guest_user': None,
                    'is_private': 'protected', # Indicates if this user has chosen to protect their Tweets (in other words, if this user's Tweets are private). "protected": false
                    'languages': None,
                    'last_name': None,
                    'liked_pages': None,
                    'live_encoders': None,
                    'live_videos': None,
                    'location': 'location', # The location specified in the user's profile, if the user provided one. As this is a freeform value, it may not indicate a valid location, but it may be fuzzily evaluated when performing searches with location queries. "location": "127.0.0.1"
                    'media_count': None,
                    'meeting_for': None,
                    'metrics': 'public_metrics', # Contains details about activity for this user. "public_metrics": {"followers_count": 507902, "following_count": 1863, "tweet_count": 3561, "listed_count": 1550}
                    'middle_name': None,
                    'music': None,
                    'name': 'name', # The name of the user, as they’ve defined it on their profile. Not necessarily a person’s name. Typically capped at 50 characters, but subject to change.
                    'name_format': None,
                    'pages_with_roles': None,
                    'payment_pricepoints': None,
                    'payment.subscriptions': None,
                    'permissions': None,
                    'photos': None,
                    'posts': None,
                    'profile_pic_url': 'profile_image_url', # The URL to the profile image for this user, as shown on the user's profile. "profile_image_url": "https://pbs.twimg.com/profile_images/1267175364003901441/tBZNFAgA_normal.jpg"
                    'quotes': None,
                    'shared_login_upgrade_required_by': None,
                    'short_name': None,
                    'significant_other': None,
                    'sports': None,
                    'supports_donate_button_in_live_video': None,
                    'timeline_url': None,
                    'token_for_business': None,
                    'url': 'url', # The URL specified in the user's profile, if present.
                    'username': 'username', # The Twitter screen name, handle, or alias that this user identifies themselves with. Usernames are unique but subject to change. Typically a maximum of 15 characters long, but some historical accounts may exist with longer names.
                    'verified': 'verified', # Indicates if this user is a verified Twitter User
                    'video_upload_limits': None,
                    'videos': None
                }
            }
        }
    }