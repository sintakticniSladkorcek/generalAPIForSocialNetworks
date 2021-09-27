from pydantic import BaseModel
from typing import List, Optional

class Text(BaseModel):
    text: str # The text content that may be attributed. Defaults to "". NOTE: The maximum length of the text of a UGC Post is 3000 characters.
    # attributes: Optional[List[Attribute]] # User generated attributes in the text.
    inferred_locale: Optional[str] # The locale that may have be inferred for this text.
# There is more!

class VisibleToLn(BaseModel):
    visibility_value: str # One of CONNECTIONS, PUBLIC, LOGGED_IN, CONTAINER.

class Media(BaseModel):
    media_status: str # The status of the availability of this media. Can be the following values: PROCESSING, READY, FAILED.
    description: Text # The description of this media.
    media_url: str # URL whose content is summarized; content may not have a corresponding url for some entities. Maximum length is 8192 characters.
    title: Text # The title of this media.
# There is more! https://docs.microsoft.com/en-us/linkedin/marketing/integrations/community-management/shares/ugc-post-api?tabs=http#sharemedia

class PostOnProfileContentInside(BaseModel):
    message: Text # The message content of this share.
    media_type: str # The type of media contained within the media field of this object. Can be the following enum values: ARTICLE, IMAGE, NONE, RICH, VIDEO, LEARNING_COURSE, JOB, QUESTION, ANSWER, CAROUSEL, TOPIC, NATIVE_DOCUMENT, URN_REFERENCE, LIVE_VIDEO.
    media: Optional[List[Media]] # The media shared in this share. Can be videos, images, or articles.

class PostOnProfileContent(BaseModel):
    content_value: PostOnProfileContentInside

# Specification of a list of images that are used to generate video.
class SlideshowSpec(BaseModel):
    images_urls: List[str] # A 3-7 element array of the URLs of the images. Required.
    duration_ms: Optional[int] # The duration in milliseconds of each image. Default value is 1000.
    transition_ms: Optional[int] # The duration in milliseconds of the crossfade transition between images. Default value is 1000.
    reordering_opt_in: Optional[bool] # Default value is False.
    music_variations_opt_in: Optional[bool] # Default value is False.

# Determines the privacy settings of the photo. If not supplied, this defaults to the privacy level granted to the app in the Login dialog. This field cannot be used to set a more open privacy setting than the one granted
class PrivacyFB(BaseModel):
    allow_for: Optional[str] # The IDs of the specific users or friend lists that can see the object (as a comma-separated string).
    deny_for: Optional[str] # The IDs of the specific users or friend lists that cannot see the object (as a comma-separate string).
    custom_settings: Optional[str] # A description of the privacy settings. For custom settings, it can contain names of users, networks and friend lists.
    allow_for_category: Optional[str] # Which category of users can see the object. This field is only set when the 'value' field is CUSTOM.
    allow_for_network: Optional[str] # The ID of the network that can see the object, or 1 for all of the user's networks.
    privacy_value: str # The privacy value for the object. One of `SELF`, `NETWORKS_FRIENDS`, `FRIENDS_OF_FRIENDS`, `ALL_FRIENDS`, `EVERYONE`, `CUSTOM`.

# A set of params describing an uploaded spherical photo. This field is not required; if it is not present we will try to generate spherical metadata from the metadata embedded in the image. If it is present, it takes precedence over any embedded metadata. Please click to the left to expand this list and see more information on each parameter.
class SphericalMetadata(BaseModel):
    projection_type: str # Accepted values include equirectangular (full spherical photo), cylindrical (panorama), and cubestrip (also known as cubemap, e.g. for synthetic or rendered content; stacked vertically with 6 faces).
    cropped_area_image_width_pixels: int # --- In equirectangular projection: As described in Google Photo Sphere XMP Metadata spec. --- In cylindrical projection: Very similar to equirectangular. This value should be equal to the actual width of the image, and together with FullPanoWidthPixels, it describes the horizontal FOV of content of the image: HorizontalFOV = 360 * CroppedAreaImageWidthPixels / FullPanoWidthPixels. --- In cubestrip projection: This has no relationship to the pixel dimensions of the image. It is simply a representation of the horizontal FOV of the content of the image. HorizontalFOV = CroppedAreaImageWidthPixels / PixelsPerDegree, where PixelsPerDegree is defined by FullPanoWidthPixels.
    cropped_area_image_height_pixels: int # --- In equirectangular projection: As described in Google Photo Sphere XMP Metadata spec. --- In cylindrical projection: This value will NOT be equal to the actual height of the image. Instead, together with FullPanoHeightPixels, it describes the vertical FOV of the image: VerticalFOV = 180 * CroppedAreaImageHeightPixels / FullPanoHeightPixels. In other words, this value is equal to the CroppedAreaImageHeightPixels value that this image would have, if it were projected into equirectangular format while maintaining the same FullPanoWidthPixels. --- In cubestrip projection: This has no relationship to the pixel dimensions of the image. It is simply a representation of the vertical FOV of the content of the image. VerticalFOV = CroppedAreaImageHeightPixels / PixelsPerDegree, where PixelsPerDegree is defined by FullPanoWidthPixels.
    full_pano_width_pixels: int # --- In equirectangular projection: As described in Google Photo Sphere XMP Metadata spec. --- In cylindrical projection: Very similar to equirectangular. This value defines a ratio of horizontal pixels to degrees in the space of the image, and in general the pixel to degree ratio in the scope of the metadata object. Concretely, PixelsPerDegree = FullPanoWidthPixels / 360. This is also equivalent to the circumference of the cylinder used to model this projection. --- In cubestrip projection: This value has no relationship to the pixel dimensions of the image. It only defines the pixel to degree ratio in the scope of the metadata object. It represents the number of pixels in 360 degrees, so pixels per degree is then given by: PixelsPerDegree = FullPanoWidthPixels / 360. As an example, if FullPanoWidthPixels were chosen to be 3600, we would have PixelsPerDegree = 3600 / 360 = 10. An image with a vertical field of view of 65 degrees would then have a CroppedAreaImageHeightPixels value of 65 * 10 = 650.
    full_pano_height_pixels: int # --- In equirectangular projection: As described in Google Photo Sphere XMP Metadata spec. --- In cylindrical projection: This value is equal to the FullPanoHeightPixels value that this image would have, if it were projected into equirectangular format while maintaining the same FullPanoWidthPixels. It is always equal to FullPanoWidthPixels / 2. --- In cubestrip projection: This value has no relationship to the pixel dimensions of the image. It is a second, redundant representation of PixelsPerDegree. FullPanoHeightPixels = 180 * PixelsPerDegree. It must be consistent with FullPanoWidthPixels: FullPanoHeightPixels = FullPanoWidthPixels / 2.
    cropped_area_left_pixels: Optional[int] = 0 # --- In equirectangular projection: As described in Google Photo Sphere XMP Metadata spec. --- In cylindrical projection: This value is equal to the CroppedAreaLeftPixels value that this image would have, if it were projected into equirectangular format while maintaining the same FullPanoWidthPixels. It is just a representation of the same angular offset that it represents in equirectangular projection in the Google Photo Sphere spec. Concretely, AngularOffsetFromLeftDegrees = CroppedAreaLeftPixels / PixelsPerDegree, where PixelsPerDegree is defined by FullPanoWidthPixels. --- In cubestrip projection: This value has no relationship to the pixel dimensions of the image. It is just a representation of the same angular offset that it represents in equirectangular projection in the Google Photo Sphere spec. AngularOffsetFromLeftDegrees = CroppedAreaLeftPixels / PixelsPerDegree, where PixelsPerDegree is defined by FullPanoWidthPixels.
    cropped_area_top_pixels: Optional[int] = 0 # --- In equirectangular projection: As described in Google Photo Sphere XMP Metadata spec. --- In cylindrical projection: This value is equal to the CroppedAreaTopPixels value that this image would have, if it were projected into equirectangular format while maintaining the same FullPanoWidthPixels. It is just a representation of the same angular offset that it represents in equirectangular projection in the Google Photo Sphere spec. Concretely, AngularOffsetFromTopDegrees = CroppedAreaTopPixels / PixelsPerDegree, where PixelsPerDegree is defined by FullPanoWidthPixels. --- In cubestrip projection: This value has no relationship to the pixel dimensions of the image. It is just a representation of the same angular offset that it represents in equirectangular projection in the Google Photo Sphere spec. AngularOffsetFromTopDegrees = CroppedAreaTopPixels / PixelsPerDegree, where PixelsPerDegree is defined by FullPanoWidthPixels.
    pose_heading_degrees: Optional[float]
    pose_pitch_degrees: Optional[float]
    pose_roll_degrees: Optional[float]
    initial_view_heading_degrees: Optional[float]
    initial_view_pitch_degrees: Optional[float]
    initial_vertical_FOV_degrees: Optional[float] # You can set the intial vertical FOV of the image. You can set either this field or InitialHorizontalFOVDegrees.
    initial_horizontal_FOV_degrees: Optional[float] # You can set the intial horizontal FOV of the image. You can set either this field or InitialVerticalFOVDegrees.
    pre_processor_crop_left_pixels: Optional[int]
    pre_processor_crop_right_pixels: Optional[int]

# Tags on a photo
class TagOnPhoto(BaseModel):
    tag_uid: Optional[str]# ID of the user to tag. Either this or tag_text are required.
    tag_text: Optional[str] # A text string to tag. Either this or tag_uid are required.
    x: int # x coordinate of each tag, as a percentage offset from the left edge of the picture.
    y: int # y coordinate of each tag, as a percentage offset from the top edge of the picture.

# Fields for body of POST request to /albums/{album_id}/photos and /groups/{group_id}/photos
class PostPhoto(BaseModel):
    allow_spherical_photo: Optional[bool] # Indicates that we should allow this photo to be treated as a spherical photo. This will not change the behavior unless the server is able to interpret the photo as spherical, such as via Photosphere XMP metadata. Regular non-spherical photos will still be treated as regular photos even if this parameter is true.
    alt_text: Optional[str]# Accessible alternative description for an image
    android_key_hash: Optional[str]
    itunes_app_id: Optional[str]# This is used by the native Share dialog that's part of iOS
    attempt: Optional[int] # Number of attempts that have been made to upload this photo
    is_audience_experience: Optional[bool]
    dated: Optional[str] # A user-specified creation time for this photo
    dated_accuracy: Optional[str] # Use only the part of the dated parameter to the specified granularity
    description: Optional[str] # The description of the photo
    composer_session_id: Optional[str]
    sponsor_boost_status: Optional[int] # The status to allow sponsor directly boost the post
    feed_targeting: Optional[str]
    full_res_is_coming_later: Optional[bool]
    override_initial_view_heading_degrees: Optional[int] # Only for spherical photos. Manually specify the initial view heading in degrees from 0 to 360. This overrides any value present in the photo embedded metadata or provided in the spherical_metadata parameter
    override_initial_view_pitch_degrees: Optional[int] # Only for spherical photos. Manually specify the initial view pitch in degrees from -90 to 90. This overrides any value present in the photo embedded metadata or provided in the spherical_metadata parameter
    override_initial_view_vertical_fov_degrees: Optional[int] # Only for spherical photos. Manually specify the initial view vertical FOV in degrees from 60 to 120. This overrides any value present in the photo embedded metadata or provided in the spherical_metadata parameter
    ios_bundle_id: Optional[str]
    is_explicit_location: Optional[bool]
    is_place_tag: Optional[bool] # If set to true, the tag is a place, not a person
    is_visual_search: Optional[bool]
    manual_privacy: Optional[bool]
    no_story: Optional[bool] # If set to true, this will suppress the News Feed story that is automatically generated on a profile when people upload a photo using your app. Useful for adding old photos where you may not want to generate a story.
    offline_id: Optional[int]
    open_graph_action_type_id: Optional[str] # The Open Graph action type
    open_graph_icon_id: Optional[str] # The Open Graph icon
    open_graph_object_id: Optional[str] # The Open Graph object ID
    open_graph_phrase: Optional[str] # The Open Graph phrase
    open_graph_set_profile_badge: Optional[bool]  # Flag to set if the post should create a profile badge
    open_graph_suggestion_mechanism: Optional[str] # The Open Graph suggestion
    location_by_id: Optional[str] # Page ID of a place associated with the photo
    visible_to_fb: Optional[PrivacyFB] # Determines the privacy settings of the photo. If not supplied, this defaults to the privacy level granted to the app in the Login dialog. This field cannot be used to set a more open privacy setting than the one granted
    proxied_app_id: Optional[str]
    is_published: Optional[bool] # Set to false if you don't want the photo to be published immediately
    photos_waterfall_id: Optional[str] # Photos waterfall ID
    spherical_metadata: Optional[SphericalMetadata] # A set of params describing an uploaded spherical photo. This field is not required; if it is not present we will try to generate spherical metadata from the metadata embedded in the image. If it is present, it takes precedence over any embedded metadata. Please click to the left to expand this list and see more information on each parameter. See also the Google Photo Sphere spec for more info on the meaning of the params: https://developers.google.com/streetview/spherical-metadata
    sponsor_id: Optional[str] # Facebook Page id that is tagged as sponsor in the photo post
    sponsor_relationship: Optional[int] # Sponsor Relationship, such as Presented By or Paid PartnershipWith
    tagged_users: Optional[List[TagOnPhoto]]
    timedelta_since_dated: Optional[int] # Same as backdated_time but with a time delta instead of absolute time
    unpublished_content_type: Optional[str] # Content type of the unpublished content type. One of SCHEDULED, SCHEDULED_RECURRING, DRAFT, ADS_POST, INLINE_CREATED, PUBLISHED, REVIEWABLE_BRANDED_CONTENT.
    source_url_of_photo: Optional[str] # The URL of a photo that is already uploaded to the Internet. You can use only one of url or vault_image_id
    user_selected_tags: Optional[bool]
    vault_image_id: Optional[str] # A vault image ID to use for a photo. You can use only one of url or vault_image_id

# Fields for body of POST request to /groups/{group_id}/albums
class AlbumInGroup(BaseModel): 
    name: str # The title of the Album
    description: Optional[str] # The Album's caption. This appears below the title of the album in the Album view
    visible_to_fb: Optional[PrivacyFB] # The privacy of the Album
    make_shared_album: Optional[bool] # Ensures the created Album is a shared Album. Default value is False.
    contributors: Optional[List[int]] # Contributors to turn this into a shared album
    location_by_id: Optional[str] # The ID of a location page to tag the Album with
    location_by_name: Optional[str] # A text location of the Album for non-page locations

# Fields for body of POST request to /groups/{group_id}/photos
class GroupPost(BaseModel):
    message: Optional[str] # The main body of the post, otherwise called the status message. Either link or message must be supplied.
    link: Optional[str] # The URL of a link to attach to the post. Either link or message must be supplied. Additional fields associated with link are shown below.

# Fields for body of POST request to /posts/{post_id}/comments
class CommentOnPost(BaseModel):
    author: str # id of entity which authored the comment
    message: Text # Text of the comment. May contain attributes such as links to people and organizations.

# Fields for body of POST request to /posts/{post_id}/likes
class LikePost(BaseModel):
    author: str # Used to specify the entity performing the action. It should be represented by a urn:li:person:{id} or urn:li:organization:{id} URN.

# Fields for body of POST request to /users/{user_id}
class UpdateProfile(BaseModel):
    dismiss_local_news_megaphone: Optional[str] # Dismisses local news megaphone. One of YES, NO.
    emoji_color_pref: Optional[int] # emoji color preference
    first_name: Optional[str] # This person's first name
    last_name: Optional[str] # This person's last name
    set_local_news_notifications: Optional[str] # Preference for setting local news notifications. One of STATUS_ON, STATUS_OFF.

# Fields for body of POST request to /users/{user_id}/videos
class VideoOnProfile(BaseModel):
    video_encoded_as_form_data: Optional[str] # The video, encoded as form data. This field is required if file_url is not provided.
    video_file_chunk: Optional[str] # The video file chunk, encoded as form data. This field is required during transfer upload phase.
    audio_story_wave_animation_handle: Optional[str] # Everstore handle of wave animation used to burn audio story video
    content_category: Optional[str] # Content category of this video. One of BEAUTY_FASHION, BUSINESS, CARS_TRUCKS, COMEDY, CUTE_ANIMALS, ENTERTAINMENT, FAMILY, FOOD_HEALTH, HOME, LIFESTYLE, MUSIC, NEWS, POLITICS, SCIENCE, SPORTS, TECHNOLOGY, VIDEO_GAMING, OTHER
    description: Optional[str] # The text describing a post that may be shown in a story about it. It may include rich text information, such as entities and emojis
    sponsor_boost_status: Optional[int] # The status to allow sponsor directly boost the post.
    embeddable: Optional[bool] # Whether the video is embeddable.
    end_offset: Optional[int]
    file_size_in_bytes: Optional[int] # The size of the entire video file in bytes.
    file_url: Optional[str] # Accessible URL of a video file. Cannot be used with upload_phase.
    fisheye_video_cropped: Optional[bool] # Whether the single fisheye video is cropped or not
    vertical_fov_for_360: Optional[int] # 360 video only: Vertical field of view
    front_z_rotation: Optional[float] # The front z rotation in degrees on the single fisheye video
    guide_keyframes_data_for_360: Optional[List[List[int]]] # 360 video only: Guide keyframes data. An array of keyframes, each of which is an array of 3 or 4 elements in the following order: [video timestamp (seconds), pitch (degrees, -90 ~ 90), yaw (degrees, -180 ~ 180), field of view (degrees, 40 ~ 90, optional)], ordered by video timestamp in strictly ascending order.
    guide_enabled_for_360: Optional[bool] # 360 video only: Whether Guide is active.
    initial_heading_for_360: Optional[int] # 360 video only: Horizontal camera perspective to display when the video begins.
    initial_pitch_for_360: Optional[int] # 360 video only: Vertical camera perspective to display when the video begins.
    is_voice_clip: Optional[bool] # used to indicate that if a video is used as audio record
    no_story: Optional[bool] # If set to true, this will suppress feed and timeline story. Default value False.
    original_fov: Optional[int] # Original field of view of the source camera
    original_projection_type_for_360: Optional[str] # 360 video only: The original projection type of the 360 video being uploaded. One of equirectangular, cubemap, half_equirectangular.
    posting_to_redspace: Optional[str] # Whether the post should appear in RedSpace. One of enabled, disabled.
    visible_to_fb: Optional[PrivacyFB] # Determines the privacy settings of the video. If not supplied, this defaults to the privacy level granted to the app in the Login Dialog. This field cannot be used to set a more open privacy setting than the one granted.
    prompt_id: Optional[str] # The prompt id in prompts or purple rain that generated this post
    prompt_tracking_string: Optional[str] # The prompt tracking string associated with this video post
    react_mode_metadata: Optional[str] # This metadata is required for clip reacts feature
    referenced_sticker_id: Optional[str] # Sticker id of the sticker in the post
    video_id_to_replace: Optional[str] # The video id your uploaded video about to replace
    slideshow_spec: Optional[SlideshowSpec] # Specification of a list of images that are used to generate video.
    source_instagram_media_id: Optional[str]
    is_360: Optional[bool] # Set if the video was recorded in 360 format. Default value is False.
    sponsor_id: Optional[str] # Facebook Page id that is tagged as sponsor in the video post
    start_offset: Optional[int] # Start byte position of the file chunk.
    swap_mode: Optional[str] # Type of replacing video request. Must have value "replace".
    video_title: Optional[str] # The title of the video
    transcode_setting_properties: Optional[str] # Properties used in computing transcode settings for the video
    unpublished_content_type: Optional[str] # Type of unpublished content, such as scheduled, draft or ads_post. One of SCHEDULED, SCHEDULED_RECURRING, DRAFT, ADS_POST, INLINE_CREATED, PUBLISHED, REVIEWABLE_BRANDED_CONTENT 
    upload_phase: Optional[str] # Type of chunked upload request. One of start, transfer, finish, cancel.
    upload_session_id: Optional[str] # ID of the chunked upload session.
    video_id_original: Optional[str] 

# Fields for body of POST request to /groups/{group_id}/videos
class VideoInGroup(BaseModel):
    video_encoded_as_form_data: Optional[str] # The video, encoded as form data. This field is required if file_url is not provided.
    video_file_chunk: Optional[str] # The video file chunk, encoded as form data. This field is required during transfer upload phase.
    audio_story_wave_animation_handle: Optional[str] # Everstore handle of wave animation used to burn audio story video
    content_category: Optional[str] # Content category of this video. One of BEAUTY_FASHION, BUSINESS, CARS_TRUCKS, COMEDY, CUTE_ANIMALS, ENTERTAINMENT, FAMILY, FOOD_HEALTH, HOME, LIFESTYLE, MUSIC, NEWS, POLITICS, SCIENCE, SPORTS, TECHNOLOGY, VIDEO_GAMING, OTHER
    description: Optional[str] # The text describing a post that may be shown in a story about it. It may include rich text information, such as entities and emojis
    embeddable: Optional[bool] # Whether the video is embeddable.
    end_offset: Optional[int]
    file_size_in_bytes: Optional[int] # The size of the entire video file in bytes.
    file_url: Optional[str] # Accessible URL of a video file. Cannot be used with upload_phase.
    fisheye_video_cropped: Optional[bool] # Whether the single fisheye video is cropped or not
    vertical_fov_for_360: Optional[int] # 360 video only: Vertical field of view
    front_z_rotation: Optional[float] # The front z rotation in degrees on the single fisheye video
    guide_keyframes_data_for_360: Optional[List[List[int]]] # 360 video only: Guide keyframes data. An array of keyframes, each of which is an array of 3 or 4 elements in the following order: [video timestamp (seconds), pitch (degrees, -90 ~ 90), yaw (degrees, -180 ~ 180), field of view (degrees, 40 ~ 90, optional)], ordered by video timestamp in strictly ascending order.
    guide_enabled_for_360: Optional[bool] # 360 video only: Whether Guide is active.
    initial_heading_for_360: Optional[int] # 360 video only: Horizontal camera perspective to display when the video begins.
    initial_pitch_for_360: Optional[int] # 360 video only: Vertical camera perspective to display when the video begins.
    original_fov: Optional[int] # Original field of view of the source camera
    original_projection_type_for_360: Optional[str] # 360 video only: The original projection type of the 360 video being uploaded. One of equirectangular, cubemap, half_equirectangular.
    prompt_id: Optional[str] # The prompt id in prompts or purple rain that generated this post
    prompt_tracking_string: Optional[str] # The prompt tracking string associated with this video post
    react_mode_metadata: Optional[str] # This metadata is required for clip reacts feature
    referenced_sticker_id: Optional[str] # Sticker id of the sticker in the post
    video_id_to_replace: Optional[str] # The video id your uploaded video about to replace
    scheduled_publish_time: Optional[int] # Scheduled publish time for group posts.
    slideshow_spec: Optional[SlideshowSpec] # Specification of a list of images that are used to generate video.
    source_instagram_media_id: Optional[str]
    is_360: Optional[bool] # Set if the video was recorded in 360 format. Default value is False.
    start_offset: Optional[int] # Start byte position of the file chunk.
    swap_mode: Optional[str] # Type of replacing video request. Must have value "replace".
    video_title: Optional[str] # The title of the video
    transcode_setting_properties: Optional[str] # Properties used in computing transcode settings for the video
    unpublished_content_type: Optional[str] # Type of unpublished content, such as scheduled, draft or ads_post. One of SCHEDULED, SCHEDULED_RECURRING, DRAFT, ADS_POST, INLINE_CREATED, PUBLISHED, REVIEWABLE_BRANDED_CONTENT 
    upload_phase: Optional[str] # Type of chunked upload request. One of start, transfer, finish, cancel.
    upload_session_id: Optional[str] # ID of the chunked upload session.

# Fields for body of POST request to /posts/{post_id}/posts
# Using https://docs.microsoft.com/en-us/linkedin/marketing/integrations/community-management/shares/ugc-post-api?tabs=http
class PostOnProfile(BaseModel):
    author: str # id to associate the share with an organization or authenticated member
    content: PostOnProfileContent # Represents type-specific content of this object. For a share this is the share text and media, and for an article it is the article contents.
    state: str # One of DRAFT, PUBLISHED, PROCESSING, PROCESSING_FAILED, DELETED, PUBLISHED_EDITED, ARCHIVED.
    visible_to_ln: VisibleToLn # Visibility restrictions on content


