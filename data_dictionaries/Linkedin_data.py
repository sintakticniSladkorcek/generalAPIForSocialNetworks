class Linkedin_data():
    dict = {
        'name': 'LinkedIn',
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
                    'age_range': None,
                    'albums': None,
                    'apprequestformerrecipients': None,
                    'apprequests': None,
                    'assigned_business_asset_groups': None,
                    'birthday': None,
                    'business_users': None,
                    'businesses': None,
                    'connections': None,
                    'created_at': None,
                    'description': None,
                    'email': None,
                    'events': None,
                    'first_name_by_location': 'firstName',
                    'favorite_athletes': None,
                    'favorite_teams': None,
                    'feed': None,
                    'first_name':'localizedFirstName',
                    'gender': None,
                    'groups': None,
                    'hometown': None,
                    'id':'id',
                    'inspirational_people': None,
                    'install_type': None,
                    'installed': None,
                    'is_guest_user': None,
                    'is_private': None,
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
                    'metrics': None,
                    'middle_name': None,
                    'music': None,
                    'name': 'firstName',
                    'name_format': None,
                    'pages_with_roles': None,
                    'payment_pricepoints': None,
                    'permissions': None,
                    'photos': None,
                    'profile_picture': 'profilePicture',
                    'posts': None,
                    'quotes': None,
                    'rich_media_documents': None,
                    'shared_login_upgrade_required_by': None,
                    'short_name': None,
                    'significant_other': None,
                    'sports': None,
                    'supports_donate_button_in_live_video': None,
                    'url': None,
                    'username': None,
                    'verified': None,
                    'video_upload_limits': None,
                    'videos': None
                }
            },
            'photos': {
                'endpoint': None
            },
            'posts': {
                'endpoint': 'socialActions',
                'paths': {
                    'comments': {
                        'path': 'comments',
                        'post_fields': {
                            'author':'actor',
                            'message':'message',
                            'text': 'text',
                            'inferred_locale': 'inferredLocale'
                        }
                    },
                    'likes': {
                        'path': 'likes',
                        'post_fields': {
                            'author':'actor',
                            'post':'object'
                        }
                    }
                }
            },
            'users': {
                'endpoint': 'ugcPosts',
                'paths': {
                    'posts': {
                        'path': '',
                        'post_fields': {
                            'author': 'author',
                            'content': 'specificContent',
                            'state': 'lifecycleState',
                            'visible_to_ln': 'visibility',
                            'visibility_value':'com.linkedin.ugc.MemberNetworkVisibility',
                            'content_value':'com.linkedin.ugc.ShareContent',
                            'message':'shareCommentary',
                            'text':'text',
                            'media_type':'shareMediaCategory',
                            'media':'media',
                            'media_status':'status',
                            'inferred_locale': 'inferredLocale'
                        }
                    }
                }
            },
            'videos': {
                'endpoint': None
            }
        }
    }