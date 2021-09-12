import requests


def call_api(access_token, data_dictionary, endpoint, fields_string, id):

    url = data_dictionary['base_url'] + data_dictionary['endpoint_mapping'][endpoint]['endpoint']
    if id != None:
        url += '/' + id
    
    parameters = 'fields=' + fields_string

    if fields_string == '':
        response = requests.get(f'{url}?&access_token={access_token}')
    else:
        response = requests.get(f'{url}?{parameters}&access_token={access_token}')
    return response

