class Linkedin_data():
    dict = {
        'name': 'Linkedin',
        'base_url': 'https://api.linkedin.com/v2/',
        'endpoint_mapping': {
            'me': 'me',
            'user': '',
            'post': '',
            'comment': ''
        },
        'field_mapping': {
            'first_name_by_location': 'firstName',
            'id': 'id',
            'last_name_by_location': 'lastName',
            'first_name': 'localizedFirstName',
            'last_name': 'localizedLastName',
            'profile_picture': 'profilePicture',
            'name': 'firstName',
            'birthday': ''
        }
    }