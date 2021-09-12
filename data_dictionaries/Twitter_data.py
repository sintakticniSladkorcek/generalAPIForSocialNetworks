class Twitter_data():
    dict = {
        'name': 'Twitter',
        'base_url': 'https://api.twitter.com/2/',
        'endpoint_mapping': {
            'album': {
                'endpoint': None
            },
            'comment': {
                'endpoint': None
            },
            'event': {
                'endpoint': None
            },
            'group': {
                'endpoint': None
            },
            'live_video': {
                'endpoint': None
            },
            'me': {
                'endpoint': 'me()'
            },
            'page': {
                'endpoint': None
            },
            'post': {
                'endpoint': 'get_status()'
            },
            'user': {
                'endpoint': 'get_user()'
            }
        }
    }