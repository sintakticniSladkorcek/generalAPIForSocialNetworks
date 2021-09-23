from pydantic import BaseModel
from typing import List, Optional

class Album(BaseModel):
    allow_spherical_photo: bool=False
    alt_text: str=None
    android_key_hash: str=None
    itunes_app_id: str=None
    attempt: int=0
    is_audience_experience: bool=False
    dated: str=None
    dated_accuracy: str=None
    description: str=None
    composer_session_id: str=None
    sponsor_boost_status: int=None
    feed_targeting: str=None
    full_res_is_coming_later: bool=False
    override_initial_view_heading_degrees: int=None
    override_initial_view_pitch_degrees: int=None
    override_initial_view_vertical_fov_degrees: int=None
    ios_bundle_id: str=None
    is_explicit_location: bool=None
    is_place_tag: bool=None
    is_visual_search: bool=None
    manual_privacy: bool=False
    no_story: bool=None
    offline_id: int=0
    open_graph_action_type_id: str=None
    open_graph_icon_id: str=None 
    open_graph_object_id: str=None
    open_graph_phrase: str=None
    open_graph_set_profile_badge: bool=False
    open_graph_suggestion_mechanism: str=None
    location_by_id: str=None
    visible_to_fb: str=None
    proxied_app_id: str=None
    is_published: bool=True
    photos_waterfall_id: str=None
    scheduled_publish_time: int=None
    spherical_metadata: str=None
    sponsor_id: str=None
    sponsor_relationship: str=None
    tagged_users: list=None
    targeting: str=None
    timedelta_since_dated: int=None
    unpublished_content_type: str=None
    source_url_of_photo: str=None
    user_selected_tags: bool=False
    vault_image_id: str=None

class Text(BaseModel):
    text: str

class GroupPost(BaseModel):
    message: Optional[str] = None
    link: Optional[str] = None

class VisibleToLn(BaseModel):
    visibility_value: str

# "status": "READY",
# "description": {
#     "text": message
# },
# "originalUrl": link,
# "title": {
#     "text": link_text
# }
class Media(BaseModel):
    media_status: str


class PostOnProfileContentInside(BaseModel):
    message: Text
    media_type: str
    media: Optional[Media] = None

class PostOnProfileContent(BaseModel):
    content_value: PostOnProfileContentInside






class PostOnProfile(BaseModel):
    author: str
    content: PostOnProfileContent
    state: str
    visible_to_ln: VisibleToLn


class Demo(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []