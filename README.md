# generalAPIForSocialNetworks

By using this API you accept the Terms and Conditions af all of the included social media APIs:

- Facebook:
    - https://developers.facebook.com/devpolicy/
    - https://developers.facebook.com/terms/dfc_platform_terms/
    - https://www.facebook.com/policies_center
- LinkedIn:
    - https://legal.linkedin.com/api-terms-of-use
    - https://www.linkedin.com/legal/user-agreement
- Twitter:
    - https://developer.twitter.com/en/developer-terms
    - https://twitter.com/en/tos

## Requirements

<!-- TODO add requirements and check compatibility -->
- python 3.7.4 or higher (might work for lower python 3 versions as well but hasn't been tested yet)
- Facebook account
- Instagram account connected to your Facebook account (you can connect them following the steps published here: TODO)
- LinkedIn account
- Twitter developer account (you can apply for it here: https://developer.twitter.com/en/apply-for-access)
    - You need a verified (connected to a phone number) Twitter account
    - Note from Twitter: When applying, you will have to submit detailed use case information about your intended use of Twitter APIs. To get through the application process as quickly as possible, please make sure to be specific about what you are building. Be sure to confirm your email address at the end of the application flow, and check that email in case our team has additional questions about your application before we can approve it.
    - Since this is just an API, it won't suffice to write "using this API" as a use case, you need to specify whyt you will be using this API for. Depending on your description, the process of getting a developer account may take a few ours or up to a few days, so be specific.

## Setup

Clone this repository.

```cmd
git clone https://github.com/sintakticniSladkorcek/generalAPIForSocialNetworks.git
```

Move to the directory where the cloned code is saved.

```cmd
cd generalAPIForSocialNetworks
```

Install/upgrade, create and activate a python virtual environment. Here teh virtual environment is named `social_venv`. For Mac OS or Linux replace the last line with `source social_venv/bin/activate`.

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
Get all the credentials you'll need.
<!-- People will be building an app to use this api, so it's ok to require them to make an app on social media sites as well in order to get access tokens. -->

#### Facebook

1) Go to https://developers.facebook.com/tools/explorer/
2) Log in to your Facebook account
3) Create an app ... TO BE CONTINUED
<!-- TODO -->

#### Instagram

#### LinkedIn

1) Create a new LinkedIn application. Go to https://www.linkedin.com/developers/apps/new and fill in the required fields.
2) On `Settings` tab verify your app.
3) On `Auth` tab find your credentials: `Client ID` and `Client Secret`. Set `Redirect URL` to `TODO: ADD URL`
4) On `Products` tab select `Sign in with LinkedIn`.
5) Enter your `Client ID`, `Client Secret` and `Redirect URL` into file `ln_credentials.json`

#### Twitter

1) Log into your Twitter developer account.
2) Name your application.
3) Enter your `API_key`, `API_secret_key`, `Bearer_token` into file `tw_credentials.json`.

## APIs

### Facebook

#### Endpoints

- `me`
- `user/<USER-ID>`
- `post/<POST-ID>`
- `comment/<COMMENT-ID>`

<!-- mušter
|||||||||

Root endpopoints and their meanings (standalone endpoints)

|Endpoint|Meaning|
|---|---|
|/docs|Swagger documentation|
|/redocs|another documentation|
|/me|info about the api user|
|/user/{USER-ID}|info about user with specific id|
|||

Only Fb parameters that can return some data with permissions given are included in the list.
TODO: List fb permissons for certain data!

Equivalent if exists for that platform is in table

Instead of this table make a simpler one. These fb non-root endpoints can also be accessed via parameters so we don't need to have them all listed like that. Instead all parameters should be listed under the description of each root endpoint.

|General API<br>endpoint|<br>parameter|Facebook<br>endpoint|<br>parameter|LinkedIn<br>endpoint|<br>parameter|Twitter<br>endpoint|<br>parameter|
|---|---|---|---|---|---|---|---|
|docs||||||||
|redocs||||||||
|me||me|birthday|me||||
|me||me|id|me||||
|me||me|age_range|me||||
|me||me|email|me||||
|me||me|favorite_athletes|me||||
|me||me|favorite_teams|me||||
|me||me|first_name|me||||
|me||me|gender|me||||
|me||me|hometown|me||||
|me||me|inspirational_people|me||||
|me||me|install_type|me||||
|me||me|installed|me||||
|me||me|is_guest_user|me||||
|me||me|languages|me||||
|me||me|last_name|me||||
|me||me|link|me||||
|me||me|location|me||||
|me||me|meeting_for|me||||
|me||me|middle_name|me||||
|me||me|name|me||||
|me||me|name_format|me||||
|me||me|payment_pricepoints|me||||
|me||me|profile_pic|me||||
|me||me|quotes|me||||
|me||me|shared_login_upgrade_required_by|me||||
|me||me|short_name|me||||
|me||me|significant_other|me||||
|me||me|sports|me||||
|me||me|supports_donate_button_in_live_video|me||||
|me||me|token_for_business|me||||
|me||me|video_upload_limits|me||||
|me||me||me||||
|me||me||me||||
|||`<ALBUM-ID>`|id|||||
|||`<ALBUM-ID>`|backdated_time|||||
|||`<ALBUM-ID>`|backdated_time_granularity|||||
|||`<ALBUM-ID>`|can_upload|||||
|||`<ALBUM-ID>`|count|||||
|||`<ALBUM-ID>`|cover_photo|||||
|||`<ALBUM-ID>`|created_time|||||
|||`<ALBUM-ID>`|description|||||
|||`<ALBUM-ID>`|event|||||
|||`<ALBUM-ID>`|from|||||
|||`<ALBUM-ID>`|link|||||
|||`<ALBUM-ID>`|location|||||
|||`<ALBUM-ID>`|name|||||
|||`<ALBUM-ID>`|place|||||
|||`<ALBUM-ID>`|privacy|||||
|||`<ALBUM-ID>`|type|||||
|||`<ALBUM-ID>`|updated_time|||||
|me||me/albums|id|me||||
|me||me/albums|backdated_time|me||||
|me||me/albums|backdated_time_granularity|me||||
|me||me/albums|can_upload|me||||
|me||me/albums||me||||
|me||me/albums||me||||
|me||me/albums||me||||
|me||me/albums||me||||
|me||me/albums||me||||
|me||me/albums||me||||
|me||me/albums||me||||
|me||me/albums||me||||
|me||me/apprequestformerrecipients||me||||
|me||me/apprequests||me||||
|me||me/business_users||me||||
|me||me/businesses||me||||
|me||me/conversations||me||||
|me||me/accounts||me||||
|me||me/ad_studies||me||||
|me||me/adaccounts||me||||
|me||me/assigned_ad_accounts||me||||
|me||me/assigned_business_asset_groups||me||||
|me||me/assigned_pages||me||||
|me||me/assigned_product_catalogs||me||||
|me||me/custom_labels||me||||
|me||me/events||me||||
|me||me/feed||me||||
|me||me/friends||me||||
|me||me/groups||me||||
|me||me/ids_for_apps||me||||
|me||me/ids_for_business||me||||
|me||me/ids_for_pages||me||||
|me||me/likes||me||||
|me||me/live_encoders||me||||
|me||me/live_videos||me||||
|me||me/music||me||||
|me||me/payment.subscriptions||me||||
|me||me/payment_transactions||me||||
|me||me/permissions||me||||
|me||me/personal_ad_accounts||me||||
|me||me/photos||me||||
|me||me/picture||me||||
|me||me/posts||me||||
|me||me/rich_media_documents||me||||
|me||me/videos||me||||
|me||me||me||||
|||||||||
|||||||||


Connections for `me`:albums, apprequestformerrecipients, apprequests, business_users, businesses, conversations, accounts, ad_studies, adaccounts, assigned_ad_accounts, assigned_business_asset_groups, assigned_pages, assigned_product_catalogs, custom_labels, events, feed, friends, groups, ids_for_apps, ids_for_business, ids_for_pages, likes, live_encoders, live_videos, music, payment.subscriptions, payment_transactions, permissions, personal_ad_accounts, photos, picture, posts, rich_media_documents, videos

Connections for `<ALBUM-ID>`:comments, likes, photos, picture

Connections for ``:
Connections for ``:
Connections for ``:
Connections for ``:
Connections for ``:
 -->

### Errors

#### Errors returned by generalAPIForSocialNetworks

If the request isn't formatted correctly, an error will be returned. The request won't be forwarded to any of the social media APIs and no data will be returned aside from the above mentioned error. You can see an example of such error below.

```json
{
    "Error": {
        "HTTPstatus": 400,
        "error_code": 1,
        "message": "Too many requested social media plaforms. To get elements by id, specify only one social media platform at the time in the parameter \'sm\'."
    }
}
```

See all possible errors in the following table.

|Status|Error code|Name|What to do|
|---|---|---|---|
|400|1|Too many requested platforms|Specify only one requested social media platform in the `sm` parameter|
||||


#### Errors returned by social media APIs

When any of the social media APIs return an error response (with HTTP status code >= 400), that response will be listed in the response of the generalAPIForSocialNetworks under the key `errors`. Responses from the other social media APIs won't be affected. An example response is shown below.

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

See the documentation about specific errors here:

- Facebook: https://developers.facebook.com/docs/graph-api/guides/error-handling/
- Instagram: https://developers.facebook.com/docs/instagram-api/reference/error-codes/
- LinkedIn: https://docs.microsoft.com/en-us/linkedin/shared/api-guide/concepts/error-handling
- Twitter: https://developer.twitter.com/en/support/twitter-api/error-troubleshooting
