import requests


def call_api(access_token, data_dictionary, method, endpoint, fields_string, id):

    url = data_dictionary['base_url'] + data_dictionary['endpoint_mapping'][endpoint]['endpoint']
    if id != None:
        url += '/' + id
    
    parameters = 'fields=' + fields_string

    if method == 'get':
        if fields_string == '':
            response = requests.get(f'{url}?&access_token={access_token}')
        else:
            response = requests.get(f'{url}?{parameters}&access_token={access_token}')
    elif method == 'post':
        response = None # TODO
    elif method == 'delete':
        response = None # TODO

    
    return response

