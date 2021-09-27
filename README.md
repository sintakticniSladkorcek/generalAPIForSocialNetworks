# General API for Social Networks

General API for Social Networks is an API that connects to different social media APIs in order to ease the developer's job of communicating to all these APIs. It saves developer the hurdle of reading documentation for and implementing calls to multiple APIs as they can now just study and integrate with one. General API for Social Networks is built using [FastAPI](https://fastapi.tiangolo.com/).

<a name="currently_supported_apis"></a>Currently supported APIs:

- [Facebook Graph API v12.0](https://developers.facebook.com/docs/graph-api)
- [Instagram Basic Display API v12.0](https://developers.facebook.com/docs/instagram-basic-display-api/)
- [LinkedIn Consumer Solutions Platform v2](https://docs.microsoft.com/en-us/linkedin/consumer/)
- [Twitter API v2](https://developer.twitter.com/en/docs/twitter-api)

Functionality:

- for Facebook:
  - retrieve data about athenticated user
  - retrieve authenticated user's posts, links, photos, videos, live videos, albums, events, groups
  - create posts in group
  - post photos, videos and live videos in events, groups and on user's profile
  - modify user's profile, video and live video
  - delete user's photos, videos and live videos
- for Instagram:
  - retrieve authenticated user's profile, photos, videos and carousels (as `albums`)
- for LinkedIn:
  - retrieve authenticated member's name and profile picture
  - post on authenticated member's profile
  - comment and like posts on behalf of an authenticated member
- for Twitter:
  - retrieve data about users
  - retrieve tweets
  - like and retweet tweets on behalf of an authenticated user

Functionality is currently limited to the functionality platforms offer free of charge and without a review process.

## Table of contents

- [General API for Social Networks](#general-api-for-social-networks)
  - [Table of contents](#table-of-contents)
  - [Requirements](#requirements)
    - [Legal](#legal)
    - [Technical](#technical)
  - [Setup](#setup)
  - [Prepare credentials](#prepare-credentials)
    - [Facebook credentials](#facebook-credentials)
    - [Instagram](#instagram)
    - [LinkedIn](#linkedin)
    - [Twitter](#twitter)
  - [Run](#run)
  - [Usage](#usage)
    - [Response](#response)
      - [Response from GET request](#response-from-get-request)
      - [Response from POST or DELETE request](#response-from-post-or-delete-request)
    - [Request](#request)
    - [Important Query String Parameters](#important-query-string-parameters)
      - [sm (required)](#sm-required)
      - [fields (optional)](#fields-optional)
      - [limit (optional)](#limit-optional)
      - [visible_to](#visible_to)
    - [Endpoints](#endpoints)
      - [/docs or /redoc](#docs-or-redoc)
      - [/auth](#auth)
      - [/ig_auth and /ln_auth](#ig_auth-and-ln_auth)
      - [Table of endpoints](#table-of-endpoints)
      - [GET /albums/{album_id}](#get-albumsalbum_id)
      - [GET /events/{event_id}](#get-eventsevent_id)
      - [GET /groups/{group_id}](#get-groupsgroup_id)
      - [GET /links/{link_id}](#get-linkslink_id)
      - [GET /live_videos/{video_id}](#get-live_videosvideo_id)
      - [GET /me](#get-me)
      - [GET /photos/{photo_id}](#get-photosphoto_id)
      - [GET /posts/{post_id}](#get-postspost_id)
      - [GET /users/{user_id}](#get-usersuser_id)
      - [GET /videos/{video_id}](#get-videosvideo_id)
      - [POST /albums/{album_id}/photos](#post-albumsalbum_idphotos)
      - [POST /groups/{group_id}/albums](#post-groupsgroup_idalbums)
      - [POST /groups/{group_id}/live_videos](#post-groupsgroup_idlive_videos)
      - [POST /groups/{group_id}/photos](#post-groupsgroup_idphotos)
      - [POST /groups/{group_id}/videos](#post-groupsgroup_idvideos)
      - [POST /live_videos/{video_id}](#post-live_videosvideo_id)
      - [POST /posts/{post_id}/comments](#post-postspost_idcomments)
      - [POST /posts/{post_id}/likes](#post-postspost_idlikes)
      - [POST /users/{user_id}](#post-usersuser_id)
      - [POST /users/{user_id}/live_videos](#post-usersuser_idlive_videos)
      - [POST /users/{user_id}/posts](#post-usersuser_idposts)
      - [POST /users/{user_id}/videos](#post-usersuser_idvideos)
      - [POST /videos/{video_id}](#post-videosvideo_id)
      - [DELETE /live_videos/{video_id}](#delete-live_videosvideo_id)
      - [DELETE /photos/{photo_id}](#delete-photosphoto_id)
      - [DELETE /videos/{video_id}](#delete-videosvideo_id)
    - [Errors](#errors)
      - [Errors returned by General API for Social Networks](#errors-returned-by-general-api-for-social-networks)
      - [Errors returned by social media APIs](#errors-returned-by-social-media-apis)
  - [Further development](#further-development)
    - [Adding another social media API](#adding-another-social-media-api)
      - [1) Choose an abbreviation](#1-choose-an-abbreviation)
      - [2) Set up authentication](#2-set-up-authentication)
      - [3) Prepare mappings](#3-prepare-mappings)
      - [4) Set up API calls](#4-set-up-api-calls)
      - [5) Update documentation](#5-update-documentation)
    - [Suggested improvements on the current version](#suggested-improvements-on-the-current-version)

## Requirements

### Legal

<a name="legal_requirements"></a>
By using this API you accept the Terms and Conditions of all of the included social media APIs:

- Facebook:
  - https://developers.facebook.com/devpolicy/
  - https://developers.facebook.com/terms/dfc_platform_terms/
  - https://www.facebook.com/policies_center
- Instagram\*:
  - https://developers.facebook.com/terms
  - https://developers.facebook.com/devpolicy/
- LinkedIn:
  - https://legal.linkedin.com/api-terms-of-use
  - https://www.linkedin.com/legal/user-agreement
- Twitter:
  - https://developer.twitter.com/en/developer-terms
  - https://twitter.com/en/tos

\*this is not a mistake, links for Instagram are in fact located at facebook.com (Instagram is owned by Facebook).

### Technical

<a name="techincal_requirements"></a>

- python 3.7.4 or higher (might work for lower python 3 versions as well but hasn't been tested yet)
- Facebook user account
- Instagram user account
- LinkedIn user account
- LinkedIn page for your application (can be added in the process of acquiring the credentials)
- verified Twitter account

## Setup

Clone this repository.

```cmd
git clone https://github.com/sintakticniSladkorcek/generalAPIForSocialNetworks.git
```

Move to the directory where the cloned code is saved.

```cmd
cd generalAPIForSocialNetworks
```

Install/upgrade, create and activate a python virtual environment. Here the virtual environment is named `social_venv`. For Mac OS or Linux replace the last line with `source social_venv/bin/activate`.

```cmd
pip install -U virtualenv
virtualenv social_venv
social_venv/Scripts/activate
```

Install all required packages by running the following command.

```cmd
pip install -r requirements.txt
```
<!-- TODO: pip freeze > requirements.txt -->
Now let's create certificate for HTTPS. For this, you need to have [Chocolatey](https://chocolatey.org/) installed. Run the following command:

```cmd
choco install mkcert
mkcert -install
mkcert localhost 127.0.0.1 ::1
```

Rename `localhost+2.pem` to `cert.pem` and `localhost+2-key.pem` to `key.pem`.

## Prepare credentials

<a name="prepare_credentials"></a>
In order to use this API you'll need to provide the same credentials as you would have to if you just used any of the social media APIs on their own. Save credentials in the appropriate json file (`{social_media_short_name}_credentials.json`). Remember that credentials are just like a username and password and should not be shared with anyone.
<!-- People will be building an app to use this api, so it's ok to require them to make an app on social media sites as well in order to get access tokens. Otherwise my app's tokens are exposed -->

### Facebook credentials

You will need an `app token`, `app secret`, `redirect uri` and a `app display name` for Facebook API. To be able to get them, you'll need a Facebook account first, then Facebook Developer account and finnaly, an app on Facebook for Developers platform.

1) To create Facebook developer account, follow [this guide from Facebook](https://developers.facebook.com/docs/development/register/).
2) To create an app, follow [this guide from Facebook](https://developers.facebook.com/docs/development/create-an-app).
3) Staying in the App Dashboard, go to *Settings*. In the section *Basic*, you can find `App ID`, `App Secret` and `Display Name`. Copy them into file `fb_credentials.json`.
4) In the field *App Domains*, set the value to `localhost` and set the `redirect_uri` value in `fb_credentials.json` to `https://localhost:443`.


### Instagram

To use Instagrams API, you'll need an app on Facebook for Developers platform, steps are described above in the first 3 steps of the instructions for obtaining Facebook credentials. Then, you will need `client_id`, `client_secret` and `redirect_uri`.

1) Follow the steps 1) - 3) from the list above.
2) In the Dashbord, find card Instagram Basic Display and click *Set Up*.
3) You will be taken to Basic Display section, where you'll see a warning in red saying to update your settings. Click on the blue button below that, that says *Create New App*.
4) Set the name for your app and click *Create App*.
5) You will be redirected to Basic Display section again, where you can now find `client_id` as *Instagram App ID* and `client_secret` as *Instagram App Secret*. Paste both into file `ig_credentials.json`.
6) Scroling down a bit, find section *Client OAuth Settings* and set up value for `redirect_uri` to `https://localhost:443/ig_auth`. Paste the same link to `ig_credentials.json`.
7) Fill in also the fields `Deauthorize Callback URL` and `Data Deletion Request URL` with values `https://localhost:443/ig_deauth` and `https://localhost:443/ig_delete_data` respectively. For now, you can also set it to any other redirect uri as the `/ig_deauth` and `/ig_delete_data` endpoints aren't yet implemented. Either way, you have to fill in these fields so you can then click the button `Save changes` and the `redirect_uri` goes into effect.
8) Go to Roles and add your Instgram handle as the Instgaram Tester.
9) Go to https://www.instagram.com/accounts/manage_access/, click *Tester Invites* and accept an invite. Without completing steps 7) and 8), authentication fails with error `{"error_type": "OAuthException", "code": 400, "error_message": "Insufficient developer role"}`.

### LinkedIn

For LinkedIn authentication we will be using [3-legged OAuth authorization code flow](https://docs.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow?context=linkedin%2Fcontext&tabs=HTTPS) for which you will need `client ID` and `client secret`. You also have to set the `redirect uri`, that has to match the one set in your LinkedIn application.

1) Create a new LinkedIn application by going to https://www.linkedin.com/developers/apps/new and filling in the required fields.
2) Verify your app in the *Settings* tab by clicking the blue *Verify* button.
3) Head over to *Auth* tab and copy your credentials: `client ID` and `client secret`. Paste them into file `ln_credentials.json`.
4) In the *Products* tab, enable *Sign in with LinkedIn* by clicking the blue *Select* button next to it.
5) Go back to the *Auth* tab to the *OAuth 2.0 settings* section and add a redirect url `https://127.0.0.1:443/ln_auth` under *Authorized redirect URLs for your app*. Copy the url you added and paste it into file `ln_credentials.json` as it has to match in both locations in order for authentication to go through.

### Twitter

For Twitter authentication you will need `consumer key`, `consumer secret key` and a `redirect uri`. We will be using [OAuth 1.0a](https://developer.twitter.com/en/docs/authentication/oauth-1-0a) with the help of the [tweepy](https://www.tweepy.org/) Twitter API wrapper.

1) Apply for your Twitter developer account here: https://developer.twitter.com/en/apply-for-access. It may take some time to get the approval. Note from Twitter: *When applying, you will have to submit detailed use case information about your intended use of Twitter APIs. To get through the application process as quickly as possible, please make sure to be specific about what you are building. Be sure to confirm your email address at the end of the application flow, and check that email in case our team has additional questions about your application before we can approve it.* Since this is just an API, it won't suffice to write "using general API for Social Networks" as a use case, you need to specify why you will be using this API for. Depending on your description, the process of getting a developer account may take a few ours or up to a few days, so be specific.
2) Go to [developer potal](https://developer.twitter.com/en/portal/dashboard) and create your application. If you're not sure how, check out [this guide from Twitter](https://developer.twitter.com/en/docs/tutorials/step-by-step-guide-to-making-your-first-request-to-the-twitter-api-v2).
3) After your app is successfully created, the *API key*, *API secret key* and *Bearer token* will be displayed. Copy the first two into file `tw_credentials.json`. If for any reason the keys don't show up or you didn't copy them, you can still access them by going to https:/[developer potal](https://developer.twitter.com/en/portal/dashboard), navigating to *Projects and Apps* in the menu on the left and selecting your application, then switching to the tab *Keys and tokens* on the top.
4) Set the `redirect uri` in `tw_credentials.json` to the uri to `oob`. Currently custom redirect aren't supported here so the value has to be `oob`.

<!-- TODO: Also accept other redirect uris? If 'oob' this, else that, try also with localhost-->

## Run

To run the General API for Social Networks, run the following command:

```cmd
python main.py
```

After that, the API can be accessed at [https://127.0.0.1:443](https://127.0.0.1:443) or [https://localhost:443](https://localhost:443). Before perfornming any calls, you'll have to authenticate with the social media with which you want to communicate. You can do this by calling GET [https://127.0.0.1:443/auth](https://127.0.0.1:443/auth) and setting the value of [`sm` parameter](#sm).

<a name="auth_example"></a>For example, to authenticate only with Facebook and LinkedIn, you would send a GET request to `https://127.0.0.1:443/auth?sm=fb,ln`.

## Usage

### Response

<!-- Naj bo requests.Response() objekt, kjer je status code odvisen tudi od tega, a je nek api vrnu error al noben -->
Response format depends on the HTTP method that was used in the request.

#### Response from GET request

Below is an example of a response of a GET request, requesting data (id, first name, last name, birthday) about the user who is logged in from Facebook, LinkedIn and Twitter. The Twitter API returned and error, so this response is in the "errors" part of the response. The other two social network APIs returned the requested data, which is grouped by requested pieces of data. We can see that LinkedIn API does not return anything for the birthday, so only the value from Facebook is returned.

```json
{
  "errors": {
    "Twitter": {
      "HTTP_status": "<Response [401]>",
      "json_response": {
        "errors": {
          "code": 89,
          "message": "Invalid or expired token."
        }
      }
    }
  },
  "id": [
    {
      "provider": "Linkedin",
      "id": "abCdefGHiJ"
    },
    {
      "provider": "Facebook",
      "id": "12345678901234567"
    }
  ],
  "first_name": [
    {
      "provider": "Linkedin",
      "localizedFirstName": "Ajda"
    },
    {
      "provider": "Facebook",
      "first_name": "Ajda"
    }
  ],
  "last_name": [
    {
      "provider": "Linkedin", 
      "localizedLastName": "Surname"
    },
    {
      "provider": "Facebook", 
      "last_name": "Surname"
    }
  ],
  "birthday": [
    {
      "provider": "Facebook", 
      "birthday": "11/29/1992"
    }
  ]
}
```

Formal definition of the response format for GET requests would therefore be:

```json
{
  "errors": {
    "<social_media_name>": {
      "HTTP_status": "<error_code>",
      "json_response": {
        "<json_response_from_social_media>"
      }
    }
  },
  "<requested_field_name>": [
    {
      "provider": "<social_media_name>",
      "<requested_field_name_in_social_media_API>": "<returned_value>"
    }
  ]
}
```

#### Response from POST or DELETE request

For now, there isn't a specific way in which our API would unify the responses from social media within the returned response. The main structure of a response for POST or DELETE request depends on success of the social media API call.

If error is present, the following structure is to be expected.

```json
{
  "errors": {
    "<social_media_name>": {
      "HTTP_status": "<error_code>",
      "json_response": {
        "<json_response_from_social_media>"
      }
    }
  },
}
```

Example:

```json
{
  "errors": {
    "Facebook": {
      "HTTP_status": "<Response [400]>", 
      "json_response": {
        "error": {
          "message": "Error validating access token: Session has expired on Wednesday, 15-Sep-21 08:00:00 PDT. The current time is Thursday, 16-Sep-21 10:16:41 PDT.", 
          "type": "OAuthException", 
          "code": 190, 
          "error_subcode": 463, 
          "fbtrace_id": "AyUUsHlS2eejfalekFTb"
        }
      }
    }
  }
}
```

If there was no error, the response would adhere to the following structure.

```json
{
  "errors": {},
  "<social_media_name>": {
    "<social_media_json_response>"
  }
}
```

Example:

```json
{
  "errors": {}, 
  "Facebook": {
    "id": "12345678901234"
  }
}
```

### Request

<!-- get, post, delete, ... -->
All requests consist of a base url `https://127.0.0.1:443`, slash `/`, an endpoint `<some_endpoint>`, question mark `?` and the required field `sm=<short_social_media_names_separated_by_comma>`. If we put this together, we get `https://127.0.0.1:443/<some_endpoint>?sm=<short_social_media_names_separated_by_comma>`.

If additional fields are specified, for GET requests append an amperstand `&` and the fields `fields=<field_names_separated_by_comma>`.
For POST requests, also append an amperstand `&` and then all of the field names and their values you want to append, separated by amperstands, like so `&<field1>=<value1>&<field2>=<value2>&<field3>=<value3> ...`.

DELETE requests don't have any fields so no additions are necessary.

Example GET request url:

```url
https://127.0.0.1:443/me?sm=fb,ln
```

Example POST request url:

```url
https://127.0.0.1:443/group/12345678901234/album?sm=fb&name=My Album&description=This is my first album
```

Example DELETE request url:

```url
https://127.0.0.1:443//videos/12345678901234?sm=fb
```

<!-- TODO: Check how is it with spaces and special characters in strings -->

### Important Query String Parameters

#### sm (required)

<a name="sm"></a>
This parameter specifies, which social media platforms do we want to include in the request. For most requests, this is a **required parameter** and at least 1 of the options has to be choosen. To choose more than 1 option, separate the values with a comma like so `sm=fb,ig`.
<!-- TODO: Add a list of requests that do not need the sm parameter. -->

Currently available values are:

- `fb` (representing Facebook),
- `ig` (representing Instagram),
- `ln` (representing LinkedIn),
- `tw` (representing Twitter).

#### fields (optional)

This parameter specifies, which fields do we want in API's response. It can be used with `GET` requests to narrow down the data in response. The parameter should be given in the following format `fields=<field_names_separated_by_comma>`, where field names are the keys form data dictionaries.

If `fields` parameter is not provided, all possible fields will be returned.

If an invalid field is requested, an error will be returned.

```json
{
  "HTTPstatus": 400,
  "error_code": 4,
  "message": "Field <field_name> is not a valid field. See data dictionaries for all available fields."
}
```

#### limit (optional)

This parameter is avilable for all `GET` requests and limits the number of results in the response for specific field. The `limit` parameter should be passed in the following format.


```txt
limit={
  "{name_of_the_field}":{integer},
  "{name_of_another_field}":{integer}
  }
```

Note that if `limit` is not provided, all data will be returned, which may take a while. Use of the `limit` parameter is therefore strongly recommended.

If the `{name_of_the_field}` won't match any of the fields specified in parameter `fields` the `limit` will not take effect. If parameter `fields` isn't provided, parameter `limit` can still be used as our API fetches all fields in case of parameter `fields` not being provided.  

If the value of `count` isn't a positive integer, the `limit` parameter won't take an effect.  

If the value of `count` isn't an integer, or `limit` parameter is otherwise malformed, an error will be returned.

```json
{
    "Error": {
        "HTTPstatus": 400,
        "error_code": 3,
        "message": "`{'<name_of_the_field>':<not an integer>}` is not a valid value. limit['<name_of_the_field>'] must be an integer. Please use the following format for the 'limit' parameter: {\"<name_of_the_field>\":<integer>}"
    }
}
```

#### visible_to

This parameter can be used with `POST` requests to set visibility of the object we are creating or updating. Since different social networks have different privacy settings, this parameter is social media specific. Use `visible_to_fb` to set who can see the object on Facebook and `visible_to_ln` for LinkedIn. 

Possible values:
- Facebook: `SELF`, `NETWORKS_FRIENDS`, `FRIENDS_OF_FRIENDS`, `ALL_FRIENDS`, `EVERYONE`, `CUSTOM`
- LinkedIn: `CONNECTIONS`, `PUBLIC`

For more, see their documentation:

- Facebook: https://developers.facebook.com/docs/graph-api/reference/privacy/, also this StackOverflow answer explains it well https://stackoverflow.com/a/37330630 
- LinkedIn: https://docs.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin?context=linkedin/consumer/context#request-body-schema


### Endpoints

<a name="endpoints"></a>
Below is a table of all of the available endpoints and paths that you can use for your requests. Each of the endpoints is additionally described in its own section. To see, which fields can be set in the `fields` parameter or as part of the `POST` request, check the fields for each endpoint in dictionaries in folder `data_dictionaries`.  

Apart from the listed endpoints, there are also some others important ones, we'll take a look at them first.

#### /docs or /redoc

These are the endpoints leading to auto-generated documentation. `/docs` leads to [Swagger UI](https://github.com/swagger-api/swagger-ui) and `/redoc` to [ReDoc](https://github.com/Redocly/redoc). Here each endpoint/path is described and all possible parameters are listed for each of them.

#### /auth

This endpoint is the one you should call first. It takes care of the authentication with all of the social media APIs so you can then perform other requests. Unless authenticated, you will not be able to perform other requests. To specify which social media APIs you want to authetnicate with, use parameter `sm`. See example [here](#auth_example).

#### /ig_auth and /ln_auth

These endpoints are used internally in the proces of authenticating with Instagram and LinkedIn, respectively. They should not be called directly by your application.

#### Table of endpoints

Endpoints for GET requests

|endpoint/path|supported social media|description|
|---|---|---|
|`/albums/{album_id}`|Facebook, Instagram|Returns data about album. For Instagram, album is collection of photos or videos in a post.|
|`/events/{event_id}`|Facebook||
|`/groups/{group_id}`|Facebook||
|`/links/{link_id}`|Facebook||
|`/live_videos/{video_id}`|Facebook||
<!-- |`/locations/{location_id}`|Facebook|| -->
|`/me`|Facebook, Instagram, LinkedIn, Twitter|Returns data about the user who is logged in.|
|`/photos/{photo_id}`|Facebook, Instagram|Returns data about photo.|
|`/posts/{post_id}`|Facebook, Twitter|Returns data about a post.|
|`/users/{user_id}`|Facebook, Instagram, Twitter|Returns data about user with given `{user_id}`.|
|`/videos/{video_id}`|Facebook, Instagram|Returns data about video.|


<!-- Add required permissions? -->
/album/{album_id}: if on user - user_photos, if on page - pages_read_engagement, if on group - you have to be admin
/comments/{comment_id}: linked to object to which the comment belongs
/events/{event_id}: if on group-A User access token of an Admin of the Event.
/groups/{group_id}: groups_access_member_info, publish_to_groups, For Public and Closed Groups-A User access token, For Secret Groups-A User access token for an Admin of the Group

Endpoints for POST requests

|endpoint/path|supported social media|description|
|---|---|---|
|`/albums/{album_id}/photos`|Facebook||
|`/groups/{group_id}/albums`|Facebook||
|`/groups/{group_id}/posts`|Facebook|Create a post in group|
|`/groups/{group_id}/live_videos`|Facebook||
|`/groups/{group_id}/photos`|Facebook||
|`/groups/{group_id}/videos`|Facebook||
|`/live_videos/{video_id}`|Facebook||
|`/posts/{post_id}/comments`|LinkedIn||
|`/posts/{post_id}/likes`|LinkedIn, Twitter||
|`/users/{user_id}`|Facebook||
|`/users/{user_id}/live_videos`|Facebook||
|`/users/{user_id}/posts`|LinkedIn, Twitter|Create a post on user's profile|
|`/users/{user_id}/videos`|Facebook||
|`/videos/{video_id}`|Facebook||

Endpoints for DELETE requests

|endpoint/path|supported social media|description|
|---|---|---|
|`/live_videos/{video_id}`|Facebook||
|`/photos/{photo_id}`|Facebook||
|`/videos/{video_id}`|Facebook||

Note that some of the available functionalities from the Facebook Graph API are not included in General API for Social Networks.

Upon a call to an unavaileble endpoint for specific social media, en error response will be returned for this social media as part of the API response.

If a nonexisting endpoint is called or none of the requested social media platforms support it, an error will be returned.

```json
{
  "Error": {
      "HTTPstatus": 400,
      "error_code": 5,
      "message": "None of the selected social media APIs are supported for the endpoint: <enpoint>."
  }
}
```

#### GET /albums/{album_id}
#### GET /events/{event_id}
#### GET /groups/{group_id}
#### GET /links/{link_id}
#### GET /live_videos/{video_id}
#### GET /me
#### GET /photos/{photo_id}
#### GET /posts/{post_id}
#### GET /users/{user_id}
#### GET /videos/{video_id}
#### POST /albums/{album_id}/photos

What does it do

Any limitations

What fields can be used in the request body
|field|data type|avaliable for|description|
|---|---|---|---|
|||||
|||||
|||||
|||||
|||||
|||||



#### POST /groups/{group_id}/albums
#### POST /groups/{group_id}/live_videos
#### POST /groups/{group_id}/photos
#### POST /groups/{group_id}/videos
#### POST /live_videos/{video_id}
#### POST /posts/{post_id}/comments
#### POST /posts/{post_id}/likes
#### POST /users/{user_id}
#### POST /users/{user_id}/live_videos
#### POST /users/{user_id}/posts
#### POST /users/{user_id}/videos
#### POST /videos/{video_id}
#### DELETE /live_videos/{video_id}
#### DELETE /photos/{photo_id}
#### DELETE /videos/{video_id}


### Errors

#### Errors returned by General API for Social Networks

If the request isn't formatted correctly, an error will be returned. The request won't be forwarded to any of the social media APIs and no data will be returned aside from the above mentioned error. You can see an example of an error response below.

```json
{
    "Error": {
        "HTTPstatus": 400,
        "error_code": 1,
        "message": "Too many requested social media plaforms. To get elements by id, specify only one social media platform at the time in the parameter \'sm\'."
    }
}
```

See all errors returned by General API for Social Networks in the following table.

|Status|Error code|Name|What to do|
|---|---|---|---|
|400|1|Too many requested platforms|Specify only one requested social media platform in the `sm` parameter|
|400|2|Invalid value for `sm`|Choose values for social media only among the [valid ones](#sm)|
|400|3|Invalid value for `limit`|Set the value following the scheme [described here](#limit-optional).|
|400|4|Invalid field in `fields`|Check for correct field names in data dictionaries.|
|400|5|`endpoint` not supported for any of the selected social networks|Check which endpoints are supported in data dictionaries.|
|400|6|`endpoint` not supported for a social media network|Check which endpoints are supported in data dictionaries.|

#### Errors returned by social media APIs

When any of the social media APIs returns an error response (with HTTP status code >= 400), that response will be listed in the response of the General API for Social Networks under the key `errors`. Responses from the other social media APIs won't be affected. An example of such response is shown below.

```json
{
  "errors": {
    "Facebook": {
      "HTTP_status": "<Response [400]>",
      "json_response": {
        "error": {
          "message": "The access token could not be decrypted",
          "type": "OAuthException",
          "code": 190,
          "fbtrace_id": "At1DQ4ehDITiJcxLyOQXnjb"
        }
      }
    }
  },
  "id": [
    {
      "provider": "Linkedin",
      "id": "cAnJ0yFHOX"
    }
  ],
  "first_name": [
    {
      "provider": "Linkedin",
      "localizedFirstName": "MyName"
    }
  ],
  "last_name": [
    {
      "provider": "Linkedin",
      "localizedLastName": "MySurname"
    }
  ]
}
```

<a name="error_documentation"></a>See the documentation about social media specific errors here:

- Facebook: https://developers.facebook.com/docs/graph-api/guides/error-handling/
- Instagram: https://developers.facebook.com/docs/instagram-api/reference/error-codes/
- LinkedIn: https://docs.microsoft.com/en-us/linkedin/shared/api-guide/concepts/error-handling
- Twitter: https://developer.twitter.com/en/support/twitter-api/error-troubleshooting

## Further development

### Adding another social media API

This is a guide on how to add a new social media API.

#### 1) Choose an abbreviation

Choose the abbreviation for the name of the social media plaform that you want to add. For example, for Facebook we used `fb`. This abbreviation will be used as the value in `sm` parameter, for naming files and functions.

Add the chosen abbreviation to `data_dictionary` in the `main.py`.

#### 2) Set up authentication

Create new json file for credentials in the rood folder of this API. Add this file to `main.py` next to

```python
file_with_fb_credentials = 'fb_credentials.json'
file_with_ig_credentials = 'ig_credentials.json'
file_with_ln_credentials = 'ln_credentials.json'
file_with_tw_credentials = 'tw_credentials.json'
```

In the folder `authentication`, add a new python file that will contain the logic for authenticating with the newly added social media.
Add the import for the main authentication function from this python file to `main.py` next to 

```python
from authentication.fb_authentication import auth as fb_auth
from authentication.ig_authentication import auth as ig_auth
from authentication.ln_authentication import auth as ln_auth
from authentication.tw_authentication import auth as tw_auth
```

and also add it to function `authenticate()` under the endpoint `/auth`.

#### 3) Prepare mappings

In folder `data_dictionaries` create a new python file. In `main.py` add an import next to other dictionary imports

```python
from data_dictionaries.Facebook_data import Facebook_data as fbd
from data_dictionaries.Instagram_data import Instagram_data as igd
from data_dictionaries.Linkedin_data import Linkedin_data as lnd
from data_dictionaries.Twitter_data import Twitter_data as twd
```

and then also add it a bit lower in the `data_dictionary`.

```python
data_dictionary = {
    'fb': fbd.dict,
    'ig': igd.dict,
    'ln': lnd.dict,
    'tw': twd.dict
}
```

Copy the contents of dictonary for some other social media API into the file ypu created in `data_dictionaries` folder and replace values to match those of the social media API you are adding. If some field does not exist for the new social medi API, set its value to `None`.

If there are new fields you would like to add, it is a bit more complicated. You have to add it to dictionaries for all of the social medi APIs and then if they are used in POST requests, add them as function parameters for a particular endpoint as well.

#### 4) Set up API calls

In the folder `social_media_api_calls`, create a new python file that will contain the code for calling the social media API. Add the import for the main call function from this python file to `main.py` next to

```python
from social_media_api_calls.facebook_api_calls import call_api as call_fb_api
from social_media_api_calls.instagram_api_calls import call_api as call_ig_api
from social_media_api_calls.linkedin_api_calls import call_api as call_ln_api
from social_media_api_calls.twitter_api_calls import call_api as call_tw_api
```

and also add it to function `call_social_media_APIs`.

#### 5) Update documentation

In the `README.md` file, add to the sections [Currently supported APIs](#currently_supported_apis), [Legal requirements](#legal_requirements), [Technical requirements](#techincal_requirements), [Prepare credentials](#prepare_credentials), [Parameter sm](#sm), [Endpoints](#endpoints) and [Error documentation for social media APIs](#error_documentation).

### Suggested improvements on the current version

<!-- -  Also now all of the data has to be saved in files, maybe it would be better to make it so that all the neccessary data is passed via call to /auth.
- If too much time, implement parameter "group_by" that allows you to either group by data first or by provider first.
- When you query, the app checks if all permissions are avaliable and if not it asks you for the permission - aka prompts login and creates access token
- Beginning with SDK v13.0 for iOS and Android, set to release in early 2022, a Client Token will be required for all calls to the Graph API. https://developers.facebook.com/docs/facebook-login/access-tokens/
- Add suggestions on how to resolve the error in the merged response. Either from the docs of social media APIs or from us if it's something with this api.
- expansion/multiple requests in one https://developers.facebook.com/docs/graph-api/field-expansion/
- Add Facebook's edges also as endpoints, not just as fields
- Create data dictionaries on the go from csv tables for each endpoint (easier to update/add/remove an endpoint or field)
- fields=all-sth Make it possible to instead of specifying all e.g. 33 fields out of 35, we just say all but not this and that. -->


<!-- # FURTHER DEVELOPMENT: Put instead of Post for updating stuff
# FURTHER DEVELOPMENT: Also now all of the data has to be saved in files, maybe it would be better to make it so that all the neccessary data is passed via call to /auth.
# FURTHER DEVELOPMENT: If too much time, implement parameter "group_by" that allows you to either group by data first or by provider first.
# FURTHER DEVELOPMENT: When you query, the app checks if all permissions are avaliable and if not it asks you for the permission - aka prompts login and creates access token
# FURTHER DEVELOPMENT: Beginning with SDK v13.0 for iOS and Android, set to release in early 2022, a Client Token will be required for all calls to the Graph API. https://developers.facebook.com/docs/facebook-login/access-tokens/
# FURTHER DEVELOPMENT: Add suggestions on how to resolve the error in the merged response. Either from the docs of social media APIs or from us if it's something with this api.
# FURTHER DEVELOPMENT: expansion/multiple requests in one https://developers.facebook.com/docs/graph-api/field-expansion/
# FURTHER DEVELOPMENT: Add Facebook's edges also as endpoints, not just as fields
# FURTHER DEVELOPMENT: Create data dictionaries on the go from csv tables for each endpoint (easier to update/add/remove an endpoint or field)
# FURTHER DEVELOPMENT: fields=all-sth Make it possible to instead of specifying all e.g. 33 fields out of 35, we just say all but not this and that.
# FURTHER DEVELOPMENT: If no fields are provided in get request, use not all of them but all that are non None value for requested sm.
# FURTHER DEVELOPMENT: Add this type (fb): /search?type=adinterest&q=TEDx -->