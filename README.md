# generalAPIForSocialNetworks

## Requirements

TODO
- python
- Facebook account
- LinkedIn account

## Setup

Clone this repository.

```cmd
git clone https://github.com/sintakticniSladkorcek/generalAPIForSocialNetworks.git
```

Move to the directory in which your cloned code is saved.

```cmd
cd generalAPIForSocialNetworks
```

Install/upgrade, create and activate a python virtual environment. Here it's called `social_venv`. For Mac OS or Linux replace the last line with `source social_venv/bin/activate`.

```cmd
pip install -U virtualenv
virtualenv social_venv
social_venv/Scripts/activate

```

Install all required packages by running the following command.

```cmd
pip install -r requirements.txt
```

<!-- pip freeze > requirements.txt -->
Get all the credentials you'll need.

### Facebook

### Instagram

### LinkedIn

1) Create a new LinkedIn application. Go to https://www.linkedin.com/developers/apps/new and fill in the required fields.
2) On `Settings` tab verify your app.
3) On `Auth` tab find your credentials: `Client ID` and `Client Secret`. Set `Redirect URL` to `TODO: ADD URL`
4) On `Products` tab select `Sign in with LinkedIn`.
5) Enter your `Client ID`, `Client Secret` and `Redirect URL` into file ln_credentials.json

### Twitter
