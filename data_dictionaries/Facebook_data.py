class Facebook_data():
    dict = {
        'name': 'Facebook',
        'base_url': 'https://graph.facebook.com/v11.0/',
        'endpoint_mapping': {
            'albums': {
                'endpoint': '',
                'get_fields': {
                    'album_type': 'type',
                    'author': 'from',
                    'can_upload_photos': 'can_upload',
                    'comments': 'comments',
                    'count': 'count',
                    'cover_photo_id': 'cover_photo', # not for albums in groups
                    'created_time': 'created_time',
                    'dated': 'backdated_time', #
                    'dated_accuracy': 'backdated_time_granularity', #
                    'description': 'description',
                    'event_on_location': 'event', #
                    'id': 'id',
                    'likes': 'likes',
                    'album_url': 'link',
                    'location_by_id': 'place', #
                    'location_by_name': 'location', #
                    'name': 'name',
                    'photos': 'photos',
                    'updated_time': 'updated_time',
                    'visible_to': 'privacy' #
                },
                'paths': {
                    'photos': {
                        'path': 'photos',
                        'post_fields': {
                            'allow_spherical_photo': 'allow_spherical_photo',
                            'alt_text': 'alt_text_custom',
                            'android_key_hash': 'android_key_hash',
                            'itunes_app_id': 'application_id',
                            'attempt': 'attempt',
                            'is_audience_experience': 'audience_exp',
                            'dated': 'backdated_time',
                            'dated_accuracy': 'backdated_time_granularity',
                            'description': 'caption',
                            'composer_session_id': 'composer_session_id',
                            'sponsor_boost_status': 'direct_share_status',
                            'feed_targeting': 'feed_targeting',
                            'full_res_is_coming_later': 'full_res_is_coming_later',
                            'override_initial_view_heading_degrees': 'initial_view_heading_override_degrees',
                            'override_initial_view_pitch_degrees': 'initial_view_pitch_override_degrees',
                            'override_initial_view_vertical_fov_degrees': 'initial_view_vertical_fov_override_degrees',
                            'ios_bundle_id': 'ios_bundle_id',
                            'is_explicit_location': 'is_explicit_location',
                            'is_place_tag': 'is_explicit_place',
                            'is_visual_search': 'is_visual_search',
                            'manual_privacy': 'manual_privacy',
                            'no_story': 'no_story',
                            'offline_id': 'offline_id',
                            'open_graph_action_type_id': 'og_action_type_id',
                            'open_graph_icon_id': 'og_icon_id',
                            'open_graph_object_id': 'og_object_id',
                            'open_graph_phrase': 'og_phrase',
                            'open_graph_set_profile_badge': 'og_set_profile_badge',
                            'open_graph_suggestion_mechanism': 'og_suggestion_mechanism',
                            'location_by_id': 'place',
                            'visible_to': 'privacy',
                            'proxied_app_id': 'proxied_app_id',
                            'is_published': 'published',
                            'photos_waterfall_id': 'qn',
                            'scheduled_publish_time': 'scheduled_publish_time',
                            'spherical_metadata': 'spherical_metadata',
                            'sponsor_id': 'sponsor_id',
                            'sponsor_relationship': 'sponsor_relationship',
                            'tagged_users': 'tags',
                            'targeting': 'targeting',
                            'timedelta_since_dated': 'time_since_original_post',
                            'unpublished_content_type': 'unpublished_content_type',
                            'source_url_of_photo': 'url',
                            'user_selected_tags': 'user_selected_tags',
                            'vault_image_id': 'vault_image_id'
                        }
                    }
                }
            },
            'comments': {
                'endpoint': '',
                'get_fields': {
                    'application': 'application',
                    'attachment': 'attachment',
                    'author': 'from',
                    'can_hide': 'can_hide',
                    'can_like': 'can_like',
                    'can_remove': 'can_remove',
                    'can_reply': 'can_comment',
                    'can_reply_privately': 'can_reply_privately',
                    'comment_on_media': 'object',
                    'comments': 'comments',
                    'created_time': 'created_time',
                    'id': 'id',
                    'is_hidden': 'is_hidden',
                    'is_private': 'is_private',
                    'like_count': 'like_count',
                    'likes': 'likes',
                    'comment_url': 'permalink_url',
                    'live_broadcast_timestamp': 'live_broadcast_timestamp',
                    'parent_object': 'object',
                    'parent_comment': 'parent',
                    'private_reply_conversation': 'private_reply_conversation',
                    'reactions': 'reactions',
                    'replies_count': 'comment_count',
                    'tagged': 'message_tags',
                    'text': 'message',
                    'user_has_liked': 'user_likes'
                } # cannot get this with user access token
            },
            'events': {
                'endpoint': '',
                'get_fields': {
                    'attending_count': 'attending_count',
                    'author': 'owner',
                    'can_guests_invite': 'can_guests_invite',
                    'can_see_guest_list': 'guest_list_enabled',
                    'category': 'category',
                    'comments': 'comments',
                    'cover_photo': 'cover',
                    'declined_count': 'declined_count',
                    'description': 'description',
                    'discount_code_enabled': 'discount_code_enabled',
                    'end_time': 'end_time',
                    'event_picture': 'picture',
                    'event_times_list': 'event_times',
                    'feed': 'feed',
                    'id': 'id',
                    'interested_count': 'interested_count',
                    'is_canceled': 'is_canceled',
                    'is_draft': 'is_draft',
                    'is_online_event': 'is_online',
                    'is_page_owned': 'is_page_owned',
                    'live_videos': 'live_videos',
                    'location': 'place',
                    'maybe_count': 'maybe_count',
                    'name': 'name',
                    'noreply_count': 'noreply_count',
                    'online_event_format': 'online_event_format',
                    'online_event_third_party_url': 'online_event_third_party_url',
                    'parent_group': 'parent_group',
                    'photos': 'photos',
                    'posts': 'posts',
                    'roles': 'roles',
                    'scheduled_publish_time': 'scheduled_publish_time',
                    'start_time': 'start_time',
                    'ticket_uri': 'ticket_uri',
                    'ticket_uri_start_sales_time': 'ticket_uri_start_sales_time',
                    'ticketing_privacy_policy': 'ticketing_privacy_uri',
                    'ticketing_terms': 'ticketing_terms_uri',
                    'ticket_tiers': 'ticket_tiers',
                    'timezone': 'timezone',
                    'type': 'type', # If you remember a better name, update. This parameter tells if event is private, public, group, community or friends. who_can_attend, for_who, audience
                    'updated_time': 'updated_time',
                    'videos': 'videos'
                },
                'paths': {
                    'live_videos': {
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
            'groups': {
                'endpoint': '',
                'get_fields': {
                    'albums': 'albums',
                    'cover_photo': 'cover',
                    'company_subdomain': 'subdomain',
                    'created_time': 'created_time',
                    'description': 'description',
                    'docs': 'docs',
                    'email': 'email',
                    'events': 'events',
                    'feed': 'feed',
                    'files': 'files',
                    'group_picture': 'picture',
                    'groups': 'groups',
                    'id': 'id',
                    'is_archived': 'archived',
                    'live_videos': 'live_videos',
                    'location': 'venue',
                    'member_count': 'member_count',
                    'member_request_count': 'member_request_count',
                    'name': 'name',
                    'parent_object': 'parent',
                    'permissions': 'permissions',
                    'privacy_level': 'privacy',
                    'purpose': 'purpose',
                    'updated_time': 'updated_time',
                    'url_icon': 'icon',
                    'videos': 'videos',
                    'website': 'link'
                },
                'paths': {
                    'albums': {
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
                    'live_videos': {
                        'path': 'live_videos',
                        'post_fields': {
                            'app_id': 'attribution_app_id',
                            'app_tag': 'app_attribution_tag',
                            'content_tags': 'content_tags',
                            'custom_image_for_schedule': 'schedule_custom_profile_image',
                            'description': 'description',
                            'dont_show_on': 'post_surfaces_blacklist',
                            'enable_backup_ingest': 'enable_backup_ingest',
                            'encoding_settings_identifier': 'encoding_settings',
                            'fisheye_video_cropped': 'fisheye_video_cropped',
                            'front_z_rotation': 'front_z_rotation',
                            'game_id': 'game_id',
                            'game_specs': 'game_specs',
                            'is_360': 'is_spherical',
                            'live_encoders': 'live_encoders',
                            'original_fov': 'original_fov',
                            'planned_start_time': 'planned_start_time',
                            'projection': 'projection',
                            'save_vod': 'save_vod',
                            'spatial_audio_format': 'spatial_audio_format',
                            'status': 'status',
                            'stereoscopic_mode': 'stereoscopic_mode',
                            'stop_on_delete_stream': 'stop_on_delete_stream',
                            'video_title': 'title',
                            'visible_to': 'privacy'
                        }
                    },
                    'photos': {
                        'path': 'photos',
                        'post_fields': {
                            'allow_spherical_photo': 'allow_spherical_photo',
                            'alt_text': 'alt_text_custom',
                            'android_key_hash': 'android_key_hash',
                            'itunes_app_id': 'application_id',
                            'attempt': 'attempt',
                            'is_audience_experience': 'audience_exp',
                            'dated': 'backdated_time',
                            'dated_accuracy': 'backdated_time_granularity',
                            'description': 'caption',
                            'composer_session_id': 'composer_session_id',
                            'sponsor_boost_status': 'direct_share_status',
                            'feed_targeting': 'feed_targeting',
                            'full_res_is_coming_later': 'full_res_is_coming_later',
                            'override_initial_view_heading_degrees': 'initial_view_heading_override_degrees',
                            'override_initial_view_pitch_degrees': 'initial_view_pitch_override_degrees',
                            'override_initial_view_vertical_fov_degrees': 'initial_view_vertical_fov_override_degrees',
                            'ios_bundle_id': 'ios_bundle_id',
                            'is_explicit_location': 'is_explicit_location',
                            'is_place_tag': 'is_explicit_place',
                            'is_visual_search': 'is_visual_search',
                            'manual_privacy': 'manual_privacy',
                            'no_story': 'no_story',
                            'offline_id': 'offline_id',
                            'open_graph_action_type_id': 'og_action_type_id',
                            'open_graph_icon_id': 'og_icon_id',
                            'open_graph_object_id': 'og_object_id',
                            'open_graph_phrase': 'og_phrase',
                            'open_graph_set_profile_badge': 'og_set_profile_badge',
                            'open_graph_suggestion_mechanism': 'og_suggestion_mechanism',
                            'location_by_id': 'place',
                            'visible_to': 'privacy',
                            'proxied_app_id': 'proxied_app_id',
                            'is_published': 'published',
                            'photos_waterfall_id': 'qn',
                            'scheduled_publish_time': 'scheduled_publish_time',
                            'spherical_metadata': 'spherical_metadata',
                            'sponsor_id': 'sponsor_id',
                            'sponsor_relationship': 'sponsor_relationship',
                            'tagged_users': 'tags',
                            'targeting': 'targeting',
                            'timedelta_since_dated': 'time_since_original_post',
                            'unpublished_content_type': 'unpublished_content_type',
                            'source_url_of_photo': 'url',
                            'user_selected_tags': 'user_selected_tags',
                            'vault_image_id': 'vault_image_id'
                        }
                    }
                }
            },
            'links': {
                'endpoint': '',
                'get_fields': {
                    'author': 'from',
                    'comments': 'comments',
                    'created_time': 'created_time',
                    'description': 'description',
                    'id': 'id',
                    'likes': 'likes',
                    'link': 'link',
                    'link_icon_url': 'icon',
                    'message': 'message',
                    'name': 'name',
                    'reactions': 'reactions',
                    'thumbnail_url': 'picture'
                }
            },
            'live_videos': {
                'endpoint': '',
                'get_fields': {
                    'ad_break_config': 'ad_break_config',
                    'ad_break_failure_reason': 'ad_break_failure_reason',
                    'author': 'from',
                    'broadcast_start_time': 'broadcast_start_time',
                    'comments': 'comments',
                    'creation_time': 'creation_time',
                    'crosspost_shared_pages': 'crosspost_shared_pages',
                    'crossposted_broadcasts': 'crossposted_broadcasts',
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
                    'live_video_url': 'permalink_url',
                    'planned_start_time': 'planned_start_time',
                    'polls': 'polls',
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
                    'cross_share_to_group_ids': 'cross_share_to_group_ids'
                    'custom_image_for_schedule': 'schedule_custom_profile_image',
                    'custom_background_image_for_schedule': 'schedule_feed_background_image',
                    'custom_labels': 'custom_labels',
                    'description': 'description',
                    'direct_share_status': 'direct_share_status',
                    'donate_button_charity_id': 'donate_button_charity_id',
                    'embeddable': 'embeddable',
                    'end_live_video': 'end_live_video',
                    'is_disturbing': 'disturbing',
                    'is_manual_mode': 'is_manual_mode',
                    'live_comment_moderation_setting': 'live_comment_moderation_setting',
                    'live_encoders': 'live_encoders',
                    'master_ingest_stream_id': 'master_ingest_stream_id',
                    'location': 'place',
                    'persistent_stream_key_status': 'persistent_stream_key_status',
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
            'locations': {
                'endpoint': '',
                'get_fields': {
                    'id': 'id',
                    'geo_location': 'location',
                    'name': 'name',
                    'overall_rating': 'overall_rating'
                }
            } # requires pages_read_engagement
            'me': {
                'endpoint': 'me',
                'get_fields': {
                    'pages_with_roles':'accounts',
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
                    'liked_pages':'likes',
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
            'photos': {
                'endpoint': '',
                'get_fields': {
                    'album': 'album',
                    'alt_text': 'alt_text',
                    'alt_text_custom': 'alt_text_custom',
                    'author': 'from',
                    'can_backdate': 'can_backdate',
                    'can_delete': 'can_delete',
                    'can_tag': 'can_tag',
                    'created_time': 'created_time',
                    'dated': 'backdated_time',
                    'dated_accuracy': 'backdated_time_granularity',
                    'display_icon': 'icon',
                    'event': 'event',
                    'height': 'height',
                    'id': 'id',
                    'image_representations': 'images',
                    'image_url': 'link',
                    'image_webp_representations': 'webp_images',
                    'likes': 'likes',
                    'location': 'place',
                    'name': 'name',
                    'page_story_id': 'page_story_id',
                    'sponsor_tags': 'sponsor_tags',
                    'tagged_names': 'name_tags',
                    'target': 'target',
                    'updated_time': 'updated_time',
                    'width': 'width'
                }
            }
            'pages': {
                'endpoint': '',
                'get_fields': {},
                'paths': {
                    'live_videos': {
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
                    } # REQUIRES PAGE ACCESS TOKEN
                }
            },
            'posts': {
                'endpoint': '',
                'get_fields': {
                    'action_links': 'actions',
                    'allowed_advertising_objectives': 'allowed_advertising_objectives',
                    'application': 'application',
                    'dated': 'backdated_time',
                    'can_reply_privately': 'can_reply_privately',
                    'link_caption': 'caption',
                    'subshares': 'child_attachments',
                    'comments_mirroring_domain': 'comments_mirroring_domain',
                    'attachment_info': 'coordinates',
                    'created_time': 'created_time',
                    'description': 'description',
                    'event': 'event',
                    'attachment_expanded_height': 'expanded_height',
                    'attachment_expanded_width': 'expanded_width',
                    'feed_targeting': 'feed_targeting',
                    'author': 'from',
                    'full_size_picture': 'full_picture',
                    'attachment_height': 'height',
                    'post_type_icon': 'icon',
                    'id': 'id',
                    'instagram_eligibility': 'instagram_eligibility',
                    'post_references_app': 'is_app_share',
                    'is_eligible_for_promotion': 'is_eligible_for_promotion',
                    'is_expired': 'is_expired',
                    'is_hidden': 'is_hidden',
                    'is_inline_created': 'is_inline_created',
                    'is_instagram_eligible': 'is_instagram_eligible',
                    'is_popular': 'is_popular',
                    'is_published': 'is_published',
                    'is_360': 'is_spherical',
                    'link_description': 'link',
                    'message': 'message',
                    'tagged_profiles_in_message': 'message_tags',
                    'display_multi_share_end_card': 'multi_share_end_card',
                    'autoselect_link_order': 'multi_share_optimized',
                    'link_name': 'name',
                    'attachment_id': 'object_id',
                    'parent_post_id': 'parent_id',
                    'post_url': 'permalink_url',
                    'location_by_id': 'place',
                    'visible_to': 'privacy',
                    'promotable_id': 'promotable_id',
                    'attachment_properties': 'properties',
                    'scheduled_publish_time': 'scheduled_publish_time',
                    'shares_count': 'shares',
                    'url_to_video_file': 'source',
                    'ataus_update_type': 'status_type',
                    'post_type_description': 'story', # User updated their profile photo.
                    'tags_in_post_type_description': 'story_tags',
                    'is_user_subscribed': 'subscribed',
                    'profile_to_post_to': 'target',
                    'targeting': 'targeting',
                    'timeline_visibility': 'timeline_visibility',
                    'post_type': 'type',
                    'updated_time': 'updated_time',
                    'shared_via': 'via',
                    'video_buying_eligibility': 'video_buying_eligibility',
                    'attachment_width': 'width',
                    'attachments': 'attachments',
                    'comments': 'comments',
                    'dynamic_posts': 'dynamic_posts',
                    'picture_from_link': 'picture',
                    'reactions': 'reactions',
                    'sharedposts': 'sharedposts',
                    'sponsor_tags': 'sponsor_tags'
                }
            },
            'users': {
                'endpoint': '',
                'get_fields': {
                    'id': 'id',
                    'age_range': 'age_range',
                    'birthday': 'birthday',
                    'email': 'email',
                    'favorite_athletes': 'favorite_athletes',
                    'favorite_teams': 'favorite_teams',
                    'first_name': 'first_name',
                    'gender': 'gender',
                    'hometown': 'hometown',
                    'inspirational_people': 'inspirational_people',
                    'install_type': 'install_type',
                    'is_installed': 'installed',
                    'is_guest_user': 'is_guest_user',
                    'languages': 'languages',
                    'last_name': 'last_name',
                    'timeline_url': 'link',
                    'location': 'location',
                    'meeting_for': 'meeting_for',
                    'middle_name': 'middle_name',
                    'name': 'name',
                    'name_format': 'name_format',
                    'payment_pricepoints': 'payment_pricepoints',
                    'profile_pic_url': 'profile_pic',
                    'quotes': 'quotes',
                    'shared_login_upgrade_required_by': 'shared_login_upgrade_required_by',
                    'short_name': 'short_name',
                    'significant_other': 'significant_other',
                    'sports': 'sports',
                    'supports_donate_button_in_live_video': 'supports_donate_button_in_live_video',
                    'token_for_business': 'token_for_business',
                    'video_upload_limits': 'video_upload_limits',
                    'pages_with_roles': 'accounts',
                    'ad_studies': 'ad_studies',
                    'adaccounts': 'adaccounts',
                    'albums': 'albums',
                    'apprequests': 'apprequests',
                    'assigned_ad_accounts': 'assigned_ad_accounts',
                    'assigned_business_asset_groups': 'assigned_business_asset_groups',
                    'assigned_pages': 'assigned_pages',
                    'assigned_product_catalogs': 'assigned_product_catalogs',
                    'business_users': 'business_users',
                    'businesses': 'businesses',
                    'conversations': 'conversations',
                    'custom_labels': 'custom_labels',
                    'feed': 'feed',
                    'friends': 'friends',
                    'ids_for_apps': 'ids_for_apps',
                    'ids_for_business': 'ids_for_business',
                    'ids_for_pages': 'ids_for_pages',
                    'liked_pages': 'likes',
                    'live_encoders': 'live_encoders',
                    'live_videos': 'live_videos',
                    'music': 'music',
                    'payment.subscriptions': 'payment.subscriptions',
                    'permissions': 'permissions',
                    'personal_ad_accounts': 'personal_ad_accounts',
                    'photos': 'photos',
                    'videos': 'videos'
                },
                'post_fields': {
                    'dismiss_local_news_megaphone': 'local_news_megaphone_dismiss_status',
                    'emoji_color_pref': 'emoji_color_pref',
                    'first_name': 'firstname',
                    'last_name': 'lastname',
                    'set_local_news_notifications': 'local_news_subscription_status'
                },
                'paths': {
                    'live_videos': {
                        'path': 'live_videos',
                        'post_fields': {
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