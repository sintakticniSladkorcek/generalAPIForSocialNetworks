class Facebook_data():
    dict = {
        'name': 'Facebook',
        'base_url': 'https://graph.facebook.com/v11.0/',
        'endpoint_mapping': {
            'album': {
                'endpoint': '',
                'get_fields': {
                    'album_type': 'type',
                    'author': 'from',
                    'can_upload_photos': 'can_upload',
                    'count': 'count',
                    'cover_photo_id': 'cover_photo', # not for albums in groups
                    'created_time': 'created_time',
                    'dated': 'backdated_time', #
                    'dated_accuracy': 'backdated_time_granularity', #
                    'description': 'description',
                    'event_on_location': 'event', #
                    'id': 'id',
                    'link': 'link',
                    'location_by_id': 'place', #
                    'location_by_name': 'location', #
                    'name': 'name',
                    'updated_time': 'updated_time',
                    'visible_to': 'privacy' #
                }
            },
            'comment': {
                'endpoint': '',
                'get_fields': {
                    'attachment': 'attachment',
                    'author': 'from',
                    'can_hide': 'can_hide',
                    'can_like': 'can_like',
                    'can_remove': 'can_remove',
                    'can_reply': 'can_comment',
                    'can_reply_privately': 'can_reply_privately',
                    'comment_on_media': 'object',
                    'created_time': 'created_time',
                    'like_count': 'like_count',
                    'parent_comment': 'parent',
                    'private_reply_conversation': 'private_reply_conversation',
                    'replies_count': 'comment_count',
                    'tagged': 'message_tags',
                    'text': 'message',
                    'user_liked': 'user_likes'
                }
            },
            'event': {
                'endpoint': '',
                'get_fields': {
                    'attending_count': 'attending_count',
                    'can_guests_invite': 'can_guests_invite',
                    'category': 'category',
                    'cover_photo': 'cover',
                    'declined_count': 'declined_count',
                    'description': 'description',
                    'discount_code_enabled': 'discount_code_enabled',
                    'end_time': 'end_time',
                    'event_times_list': 'event_times',
                    'can_see_guest_list': 'guest_list_enabled',
                    'id': 'id',
                    'interested_count': 'interested_count',
                    'is_canceled': 'is_canceled',
                    'is_draft': 'is_draft',
                    'is_online_event': 'is_online',
                    'is_page_owned': 'is_page_owned',
                    'maybe_count': 'maybe_count',
                    'name': 'name',
                    'noreply_count': 'noreply_count',
                    'online_event_format': 'online_event_format',
                    'online_event_third_party_url': 'online_event_third_party_url',
                    'author': 'owner',
                    'parent_group': 'parent_group',
                    'location': 'place',
                    'scheduled_publish_time': 'scheduled_publish_time',
                    'start_time': 'start_time',
                    'ticket_uri': 'ticket_uri',
                    'ticket_uri_start_sales_time': 'ticket_uri_start_sales_time',
                    'ticketing_privacy_policy': 'ticketing_privacy_uri',
                    'ticketing_terms': 'ticketing_terms_uri',
                    'timezone': 'timezone',
                    'type': 'type', # If you remember a better name, update. This parameter tells if event is private, public, group, community or friends.
                    'updated_time': 'updated_time'
                },
                'paths': {
                    'live_video': {
                        'path': 'live_videos',
                        'post_fields': {
                            'app_id': 'attribution_app_id',
                            'content_tags': 'content_tags',
                            'custom_image_for_schedule': 'schedule_custom_profile_image',
                            'description': 'description',
                            'enable_backup_ingest': 'enable_backup_ingest',
                            'encoding_settings_identifier': 'encoding_settings',
                            'fisheye_video_cropped': 'fisheye_video_cropped',
                            'front_z_rotation': 'front_z_rotation',
                            'is_360': 'is_spherical',
                            'live_encoders': 'live_encoders',
                            'original_fov': 'original_fov',
                            'planned_start_time': 'planned_start_time',
                            'projection': 'projection',
                            'spatial_audio_format': 'spatial_audio_format',
                            'status': 'status',
                            'stereoscopic_mode': 'stereoscopic_mode',
                            'stop_on_delete_stream': 'stop_on_delete_stream',
                            'video_title': 'title',
                            'visible_to': 'privacy'
                        }
                    }
                }
            },
            'group': {
                'endpoint': '',
                'get_fields': {
                    'cover_photo': 'cover',
                    'description': 'description',
                    'email': 'email',
                    'url_icon': 'icon',
                    'id': 'id',
                    'member_count': 'member_count',
                    'member_request_count': 'member_request_count',
                    'name': 'name',
                    'parent_object': 'parent',
                    'permissions': 'permissions',
                    'privacy_level': 'privacy',
                    'updated_time': 'updated_time'
                },
                'paths': {
                    'album': {
                        'path': 'albums',
                        'post_fields': {
                            'contributors': 'contributors',
                            'description': 'description',
                            'location_by_id': 'place',
                            'location_by_name': 'location',
                            'make_shared_album': 'make_shared_album',
                            'name': 'name',
                            'visible_to': 'privacy'
                        }
                    },
                    'live_video': {
                        'path': 'live_videos',
                        'post_fields': {
                            'app_id': 'attribution_app_id',
                            'content_tags': 'content_tags',
                            'custom_image_for_schedule': 'schedule_custom_profile_image',
                            'description': 'description',
                            'enable_backup_ingest': 'enable_backup_ingest',
                            'encoding_settings_identifier': 'encoding_settings',
                            'fisheye_video_cropped': 'fisheye_video_cropped',
                            'front_z_rotation': 'front_z_rotation',
                            'is_360': 'is_spherical',
                            'live_encoders': 'live_encoders',
                            'original_fov': 'original_fov',
                            'planned_start_time': 'planned_start_time',
                            'projection': 'projection',
                            'spatial_audio_format': 'spatial_audio_format',
                            'status': 'status',
                            'stereoscopic_mode': 'stereoscopic_mode',
                            'stop_on_delete_stream': 'stop_on_delete_stream',
                            'video_title': 'title',
                            'visible_to': 'privacy'
                        }
                    }
                }
            },
            'live_video': {
                'endpoint': '',
                'get_fields': {
                    'ad_break_config': 'ad_break_config',
                    'ad_break_failure_reason': 'ad_break_failure_reason',
                    'author': 'from',
                    'broadcast_start_time': 'broadcast_start_time',
                    'copyright': 'copyright',
                    'creation_time': 'creation_time',
                    'dash_ingest_url': 'dash_ingest_url',
                    'dash_preview_url': 'dash_preview_url',
                    'description': 'description',
                    'embed_html': 'embed_html',
                    'id': 'id',
                    'ingest_streams': 'ingest_streams',
                    'is_manual_mode': 'is_manual_mode',
                    'is_reference_only': 'is_reference_only',
                    'live_encoders': 'live_encoders',
                    'live_views_count': 'live_views',
                    'overlay_url': 'overlay_url',
                    'permalink_url': 'permalink_url',
                    'planned_start_time': 'planned_start_time',
                    'seconds_left': 'seconds_left',
                    'secure_stream_url': 'secure_stream_url',
                    'status': 'status',
                    'stream_url': 'stream_url',
                    'targeting': 'targeting',
                    'video': 'video',
                    'video_title': 'title'
                },
                'post_fields': {
                    'allow_bm_crossposting': 'allow_bm_crossposting',
                    'content_tags': 'content_tags',
                    'crossposting_actions': 'crossposting_actions',
                    'custom_image_for_schedule': 'schedule_custom_profile_image',
                    'custom_background_image_for_schedule': 'schedule_feed_background_image',
                    'custom_labels': 'custom_labels',
                    'description': 'description',
                    'direct_share_status': 'direct_share_status',
                    'disturbing': 'disturbing',
                    'donate_button_charity_id': 'donate_button_charity_id',
                    'embeddable': 'embeddable',
                    'end_live_video': 'end_live_video',
                    'is_manual_mode': 'is_manual_mode',
                    'live_comment_moderation_setting': 'live_comment_moderation_setting',
                    'live_encoders': 'live_encoders',
                    'master_ingest_stream_id': 'master_ingest_stream_id',
                    'location': 'place',
                    'planned_start_time': 'planned_start_time',
                    'projection': 'projection',
                    'sponsor_id': 'sponsor_id',
                    'sponsor_relationship': 'sponsor_relationship',
                    'status': 'status',
                    'tagged_users': 'tags',
                    'targeting': 'targeting',
                    'stereoscopic_mode': 'stereoscopic_mode',
                    'stop_on_delete_stream': 'stop_on_delete_stream',
                    'video_title': 'title',
                    'visible_to': 'privacy'
                }
            },
            'me': {
                'endpoint': 'me',
                'get_fields': {
                    'accounts':'accounts',
                    'ad_studies':'ad_studies',
                    'adaccounts':'adaccounts',
                    'age_range':'age_range',
                    'albums':'albums',
                    'apprequestformerrecipients':'apprequestformerrecipients',
                    'apprequests':'apprequests',
                    'assigned_business_asset_groups':'assigned_business_asset_groups',
                    'birthday':'birthday',
                    'business_users':'business_users',
                    'businesses':'businesses',
                    'email':'email',
                    'events':'events',
                    'first_name_by_location': 'first_name',
                    'favorite_athletes':'favorite_athletes',
                    'favorite_teams':'favorite_teams',
                    'feed':'feed',
                    'first_name':'first_name',
                    'connections':'friends',
                    'gender':'gender',
                    'groups':'groups',
                    'hometown':'hometown',
                    'id':'id',
                    'inspirational_people':'inspirational_people',
                    'install_type':'install_type',
                    'installed':'installed',
                    'is_guest_user':'is_guest_user',
                    'languages':'languages',
                    'last_name':'last_name',
                    'last_name_by_location': 'last_name',
                    'likes':'likes',
                    'link':'link',
                    'live_encoders':'live_encoders',
                    'live_videos':'live_videos',
                    'location':'location',
                    'meeting_for':'meeting_for',
                    'middle_name':'middle_name',
                    'music':'music',
                    'name':'name',
                    'name_format':'name_format',
                    'payment_pricepoints':'payment_pricepoints',
                    'permissions':'permissions',
                    'personal_ad_accounts':'personal_ad_accounts',
                    'photos':'photos',
                    'profile_picture':'picture',
                    'posts':'posts',
                    'quotes':'quotes',
                    'rich_media_documents':'rich_media_documents',
                    'shared_login_upgrade_required_by':'shared_login_upgrade_required_by',
                    'short_name':'short_name',
                    'significant_other':'significant_other',
                    'sports':'sports',
                    'supports_donate_button_in_live_video':'supports_donate_button_in_live_video',
                    'video_upload_limits':'video_upload_limits',
                    'videos':'videos'
                }
            },
            'page': {
                'endpoint': 'page',
                'get_fields': {},
                'paths': {
                    'live_video': {
                        'path': 'live_videos',
                        'post_fields': {
                            'app_id': 'attribution_app_id',
                            'content_tags': 'content_tags',
                            'crossposting_actions': 'crossposting_actions',
                            'custom_image_for_schedule': 'schedule_custom_profile_image',
                            'custom_labels': 'custom_labels',
                            'description': 'description',
                            'donate_button_charity_id': 'donate_button_charity_id',
                            'enable_backup_ingest': 'enable_backup_ingest',
                            'encoding_settings_identifier': 'encoding_settings',
                            'fisheye_video_cropped': 'fisheye_video_cropped',
                            'front_z_rotation': 'front_z_rotation',
                            'game_show': 'game_show',
                            'is_360': 'is_spherical',
                            'live_encoders': 'live_encoders',
                            'original_fov': 'original_fov',
                            'planned_start_time': 'planned_start_time',
                            'products_shown': 'product_items',
                            'projection': 'projection',
                            'spatial_audio_format': 'spatial_audio_format',
                            'status': 'status',
                            'stereoscopic_mode': 'stereoscopic_mode',
                            'stop_on_delete_stream': 'stop_on_delete_stream',
                            'targeting': 'targeting',
                            'video_title': 'title',
                            'visible_to': 'privacy'
                        }
                    }
                }
            },
            'post': {
                'endpoint': ''
            },
            'user': {
                'endpoint': '',
                'get_fields': {},
                'post_fields': {},
                'paths': {
                    'live_video': {
                        'path': 'live_videos',
                        'post_fields': {
                            'app_id': 'attribution_app_id',
                            'content_tags': 'content_tags',
                            'custom_image_for_schedule': 'schedule_custom_profile_image',
                            'description': 'description',
                            'donate_button_charity_id': 'donate_button_charity_id',
                            'enable_backup_ingest': 'enable_backup_ingest',
                            'encoding_settings_identifier': 'encoding_settings',
                            'fisheye_video_cropped': 'fisheye_video_cropped',
                            'front_z_rotation': 'front_z_rotation',
                            'is_360': 'is_spherical',
                            'live_encoders': 'live_encoders',
                            'original_fov': 'original_fov',
                            'planned_start_time': 'planned_start_time',
                            'projection': 'projection',
                            'spatial_audio_format': 'spatial_audio_format',
                            'status': 'status',
                            'stereoscopic_mode': 'stereoscopic_mode',
                            'stop_on_delete_stream': 'stop_on_delete_stream',
                            'video_title': 'title',
                            'visible_to': 'privacy'
                        }
                    }
                }
            }
        }
    }