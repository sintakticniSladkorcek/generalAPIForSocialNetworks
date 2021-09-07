# generalAPIForSocialNetworks

General API for social networks is an API that connects to different social media APIs in order to ease the developer's job of communicating to all these APIs. It saves developers the hurdle of reading documentation for and implementing calls to multiple APIs as they can now just study and integrate with one.

Currently supported APIs:

- Facebook Graph API v11.0
- Instagram Basic Display API v11.0
- LinkedIn Consumer Solutions Platform v2
- Twitter API v2

Functionality:

- retrieve data about the user who is logged in
- TODO

## Requirements

### Legal

By using this API you accept the Terms and Conditions of all of the included social media APIs:

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

<!-- TODO: Add Instagram -->

### Technical

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

## Prepare credentials

In order to use this API you'll need to provide the same credentials as you would have to if you just used any of the social media APIs on their own. Save credentials in the appropriate json file (`{social_media_short_name}_credentials.json`). Remember that credentials are just like a username and password and should not be shared with anyone.
<!-- People will be building an app to use this api, so it's ok to require them to make an app on social media sites as well in order to get access tokens. Otherwise my app's tokens are exposed -->

### Facebook credentials

You will need an `app token` and a `user token` for Facebook API. To be able to get them, you'll need a Facebook account first, then Facebook Developer account and finnaly an app on Facebook for Developers platform.
<!-- TODO: Do we also need the app token? -->

1) To create Facebook developer account, follow [this guide from Facebook](https://developers.facebook.com/docs/development/register/).
2) To create an app, follow [this guide from Facebook](https://developers.facebook.com/docs/development/create-an-app).
3) Go to https://developers.facebook.com/tools/explorer, login to your Facebook account if prompted and choose your app in the *Facebook App* dropdown.
4) To get an `app token`, choose *Get App Token* in *User or Page* dropdown. Click the blue *Generate Access Token* button anc copy the token that appears in the field above the button. Paste the token into file `fb_credentials.json`.
5) To get a `user token`, choose *Get User Token* in *User or Page* dropdown. In the dropdown at the bottom, choose which permissions do you want to grant. You can read more abour permissions in `TODO` chapter. Click the blue *Generate Access Token* button anc copy the token that appears in the field above the button. Paste the token into file `fb_credentials.json`.
<!-- TODO: add link to chapter for permissions -->
<!-- fb permissions: https://developers.facebook.com/docs/permissions/reference -->

The *app token* does not expire. The *user token*, howewer, expires in 2 hours.
<!-- TODO extend and change or does our API refresh? Finish the text above based on the answer. -->

### Instagram

<!-- TODO -->

### LinkedIn

For LinkedIn authentication we will be using [3-legged OAuth authorization code flow](https://docs.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow?context=linkedin%2Fcontext&tabs=HTTPS) for which you will need `client ID` and `client secret`. You also have to set the `redirect uri`, that has to match the one set in your LinkedIn application.

1) Create a new LinkedIn application by going to https://www.linkedin.com/developers/apps/new and filling in the required fields.
2) Verify your app in the *Settings* tab by clicking the blue *Verify* button.
3) Head over to *Auth* tab and copy your credentials: `client ID` and `client secret`. Paste them into file `ln_credentials.json`.
4) In the *Products* tab, enable *Sign in with LinkedIn* by clicking the blue *Select* button next to it.
5) Go back to the *Auth* tab to the *OAuth 2.0 settings* section and add a redirect url under *Authorized redirect URLs for your app*. This can also be a postman link (https://oauth.pstmn.io/v1/callback) or a localhost link (http://127.0.0.1:8000). Copy the url you added and paste it into file `ln_credentials.json` as it has to match in both locations in order for authentication to go through.

### Twitter

For Twitter authentication you will need `consumer key`, `consumer secret key` and a `redirect uri`. We will be using [OAuth 1.0a](https://developer.twitter.com/en/docs/authentication/oauth-1-0a) with the help of the [tweepy](https://www.tweepy.org/) Twitter API wrapper.

1) Apply for your Twitter developer account here: https://developer.twitter.com/en/apply-for-access. It may take some time to get the approval. Note from Twitter: *When applying, you will have to submit detailed use case information about your intended use of Twitter APIs. To get through the application process as quickly as possible, please make sure to be specific about what you are building. Be sure to confirm your email address at the end of the application flow, and check that email in case our team has additional questions about your application before we can approve it.* Since this is just an API, it won't suffice to write "using general API for Social Networks" as a use case, you need to specify why you will be using this API for. Depending on your description, the process of getting a developer account may take a few ours or up to a few days, so be specific.
2) Go to [developer potal](https://developer.twitter.com/en/portal/dashboard) and create your application. If you're not sure how, check out [this guide from Twitter](https://developer.twitter.com/en/docs/tutorials/step-by-step-guide-to-making-your-first-request-to-the-twitter-api-v2).
3) After your app is successfully created, the *API key*, *API secret key* and *Bearer token* will be displayed. Copy the first two into file `tw_credentials.json`. If for any reason the keys don't show up or you didn't copy them, you can still access them by going to https:/[developer potal](https://developer.twitter.com/en/portal/dashboard), navigating to *Projects and Apps* in the menu on the left and selecting your application, then switching to the tab *Keys and tokens* on the top.
4) Set the `redirect uri` in `tw_credentials.json` to the uri to `oob`. Currently custom redirect aren't supported here so the value has to be `oob`.

<!-- TODO: Also accept other redirect uris? If 'oob' this, else that, try also with localhost-->

## Usage

### Response

<!-- Naj bo requests.Response() objekt, kjer je status code odvisen tudi od tega, a je nek api vrnu error al noben -->
<!-- Različn format glede na metodo (post, get, ...)? -->

### Request

<!-- get, post, delete, ... -->

### Important parameters

#### sm

This parameter specifies, which social media platforms do we want to include in the request. For most requests, this is a required parameter and at least 1 of the options has to be choosen. To choose more than 1 option, separate the values with a comma like so `sm=fb,ig`.
<!-- TODO: Add  a list of requests that do not need the sm parameter. -->

Currently available values are: `fb` (representing Facebook), `ig` (representing Instagram), `ln` (representing LinkedIn), `tw` (representing Twitter).

#### limit

Yet to be implemented.
<!-- TODO: Implement  -->
Positive integer

#### visible_to

Yet to be implemented.
<!-- TODO: Implement and add mappings (what is equivalent for each social media) -->
Available values: `me`, `connections`, `public`, `custom`(?)

### Endpoints

Below is a table of all of the available endpoints and paths that you can use for your requests. Each of the endpoints/path is additionally described in its own section. Apart from the listed endpoints, there are also some others important ones, well look at them first.

#### /docs or /redoc

These are the endpoints leading to auto-generated documentation. `/docs` leads to Swagger and `/redoc` to ___. Here each endpoint/path is described and all possible parameters are listed for each of them.

#### /auth

Yet to be implemented.

This endpoint is the one you should call first. It takes care of the authentication with all of the social media APIs so you can then perform other requests. Unless authenticated, you will not be able to perform other requests. 

<!-- Add use example and implement -->

#### Table of endpoints

|endpoint/path|supported social media|description|
|---|---|---|
|me|Facebook, LinkedIn|Returns data about the user who is logged in.|

<!-- Add required permissions? -->

<!-- Some fb non-root endpoints can also be accessed via parameters so we don't need to have them all listed like that. Instead all parameters should be listed under the description of each root endpoint. -->


<!-- Connections for `me` on fb:albums, apprequestformerrecipients, apprequests, business_users, businesses, conversations, accounts, ad_studies, adaccounts, assigned_ad_accounts, assigned_business_asset_groups, assigned_pages, assigned_product_catalogs, custom_labels, events, feed, friends, groups, ids_for_apps, ids_for_business, ids_for_pages, likes, live_encoders, live_videos, music, payment.subscriptions, payment_transactions, permissions, personal_ad_accounts, photos, picture, posts, rich_media_documents, videos

Connections for `<ALBUM-ID> on fb`:comments, likes, photos, picture -->

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
|400|2|Invalid value for `sm`|Choose values for social media only among the valid ones|

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
Add the import for the main authentication function from this python file to `main.py` and also add it under the endpoint `auth`.
<!-- TODO: Check if this is still true with /auth and add additional explanation of how-to if needed.  -->

#### 3) Prepare mappings

<!-- TODO -->

#### 4) Set up API calls

In the folder `social_media_api_calls`, create a new python file that will contain the code for calling the social media API. Add the import for the main call function from this python file to `main.py` and also add it to function `call_social_media_APIs`.

### Suggested improvements on the current version
