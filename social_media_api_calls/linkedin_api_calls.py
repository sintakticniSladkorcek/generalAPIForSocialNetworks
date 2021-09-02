import requests

def create_header(access_token):
    '''
    Prepare headers to attach to request.
    '''

    headers = {
    'Authorization': f'Bearer {access_token}',
    'cache-control': 'no-cache',
    'X-Restli-Protocol-Version': '2.0.0'
    }
    return headers


def call_api(access_token, data_dictionary, endpoint, fields_string, id):

    url = data_dictionary['base_url'] + data_dictionary['endpoint_mapping'][endpoint]
    if id != None:
        url += '/' + id

    parameters = 'fields=' + fields_string

    headers = create_header(access_token)

    if fields_string == '':
        response = requests.get(f'{url}', headers=headers)
    else:
        response = requests.get(f'{url}?{parameters}', headers=headers)
    return response
