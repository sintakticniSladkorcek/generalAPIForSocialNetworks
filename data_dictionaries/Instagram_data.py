class Instagram_data():
    dict = {
        'name': 'Instagram',
        'base_url': 'https://graph.instagram.com/v12.0/',
        'endpoint_mapping': {
            'albums': {
                'endpoint': '',
                'get_fields': {
                    'album_type': 'media_type',
                    'album_url': 'permalink',
                    'author': 'username',
                    'can_upload_photos':  None,
                    'children': 'children',
                    'comments':  None,
                    'count':  None,
                    'cover_photo_id':  None,
                    'created_time': 'timestamp',
                    'dated':  None,
                    'dated_accuracy':  None,
                    'description': 'caption',
                    'event_on_location':  None,
                    'id': 'id',
                    'likes':  None,
                    'location_by_id':  None,
                    'location_by_name':  None,
                    'name':  None,
                    'photos':  None,
                    'updated_time':  None,
                    'url_to_album': 'media_url',
                    'visible_to_fb_fb_fb': None
                },
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
            'live_videos': {
                'endpoint': None
            },
            'me': {
                'endpoint': 'me',
                'get_fields': {
                    'account_type': 'account_type',
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
                    'is_private': None,
                    'languages': None,
                    'last_name': None,
                    'last_name_by_location': None,
                    'liked_pages': None,
                    'link': None,
                    'live_encoders': None,
                    'live_videos': None,
                    'location': None,
                    'media_count': 'media_count',
                    'meeting_for': None,
                    'metrics': None,
                    'middle_name': None,
                    'music': None,
                    'name': 'username',
                    'name_format': None,
                    'pages_with_roles': None,
                    'payment_pricepoints': None,
                    'permissions': None,
                    'photos': None,
                    'profile_picture': None,
                    'posts': 'media',
                    'quotes': None,
                    'rich_media_documents': None,
                    'shared_login_upgrade_required_by': None,
                    'short_name': None,
                    'significant_other': None,
                    'sports': None,
                    'supports_donate_button_in_live_video': None,
                    'url': None,
                    'username': 'username',
                    'verified': None,
                    'video_upload_limits': None,
                    'videos': None
                }
            },
            'photos': {
                'endpoint': '',
                'get_fields': {
                    'album': None,
                    'alt_text': None,
                    'alt_text_custom': None,
                    'author': 'username',
                    'can_backdate': None,
                    'can_delete': None,
                    'can_tag': None,
                    'content_category': 'media_type',
                    'created_time': 'timestamp',
                    'dated': None,
                    'dated_accuracy': None,
                    'description': 'caption',
                    'display_icon': None,
                    'event': None,
                    'height': None,
                    'id': 'id',
                    'image_representations': None,
                    'image_url': 'permalink',
                    'image_webp_representations': None,
                    'likes': None,
                    'location': None,
                    'name': None,
                    'page_story_id': None,
                    'sponsor_tags': None,
                    'tagged_names': None,
                    'target': None,
                    'updated_time': None,
                    'url_to_image_file': 'media_url',
                    'width': None
                }
            },
            'posts': {
                'endpoint': None #maybe this one as well
            },
            'users': {
                'endpoint': '',
                'get_fields': {
                    'account_type': 'account_type',
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
                    'created_at': None,
                    'custom_labels': None,
                    'description': None,
                    'email': None,
                    'favorite_athletes': None,
                    'favorite_teams': None,
                    'feed': None,
                    'first_name': None,
                    'friends': None,
                    'gender': None,
                    'hometown': None,
                    'id': 'id',
                    'ids_for_apps': None,
                    'ids_for_business': None,
                    'ids_for_pages': None,
                    'inspirational_people': None,
                    'install_type': None,
                    'is_installed': None,
                    'is_guest_user': None,
                    'is_private': None,
                    'languages': None,
                    'last_name': None,
                    'liked_pages': None,
                    'live_encoders': None,
                    'live_videos': None,
                    'location': None,
                    'media_count': 'media_count',
                    'meeting_for': None,
                    'metrics': None,
                    'middle_name': None,
                    'music': None,
                    'name': 'username',
                    'name_format': None,
                    'pages_with_roles': None,
                    'payment_pricepoints': None,
                    'payment.subscriptions': None,
                    'permissions': None,
                    'photos': None,
                    'posts': 'media',
                    'profile_pic_url': None,
                    'quotes': None,
                    'shared_login_upgrade_required_by': None,
                    'short_name': None,
                    'significant_other': None,
                    'sports': None,
                    'supports_donate_button_in_live_video': None,
                    'timeline_url': None,
                    'token_for_business': None,
                    'url': None,
                    'username': 'username',
                    'verified': None,
                    'video_upload_limits': None,
                    'videos': None
                }
            },
            'videos': {
                'endpoint': '',
                'get_fields': {
                    'ad_breaks': None,
                    'author': 'username',
                    'captions': None,
                    'comments': None,
                    'content_category': 'media_type',
                    'content_tags': None,
                    'created_time': 'timestamp',
                    'crosspost_shared_pages': None,
                    'custom_labels': None,
                    'dated': None,
                    'dated_accuracy': None,
                    'description': 'caption',
                    'display_icon': None,
                    'embed_html': None,
                    'embeddable': None,
                    'event': None,
                    'formats': None,
                    'id': 'id',
                    'is_crosspost_video': None,
                    'is_crossposting_eligible': None,
                    'is_episode': None,
                    'is_instagram_eligible': None,
                    'is_published': None,
                    'is_reference_only': None,
                    'length': None,
                    'likes': None,
                    'live_status': None,
                    'location': None,
                    'music_video_copyright': None,
                    'post_views': None,
                    'premiere_status': None,
                    'poll_settings': None,
                    'polls': None,
                    'scheduled_publish_time': None,
                    'sponsor_tags': None,
                    'status': None,
                    'tagged_users': None,
                    'thumbnails': 'thumbnail_url',
                    'universal_video_id': None,
                    'updated_time': None,
                    'url_to_video_file': 'media_url',
                    'video_insights': None,
                    'video_title': None,
                    'video_url': 'permalink',
                    'views_count': None,
                    'visible_to_fb_fb_fb': None
                }
            }
        }        
    }