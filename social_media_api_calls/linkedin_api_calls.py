import requests
import json

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


def call_api(access_token, data_dictionary, method, endpoint, path, mapped_fields, id):
    
    url = data_dictionary['base_url'] + data_dictionary['endpoint_mapping'][endpoint]['endpoint']
    if id != None:
        id = f'urn:li:person:{id}'
        url += '/' + id
    if path != None:
        url += '/' + data_dictionary['endpoint_mapping'][endpoint]['paths'][path]['path']

    headers = create_header(access_token)

    if method == 'get':
        # remove possible duplicates
        mapped_fields = list(dict.fromkeys(mapped_fields))

        # concatenate parameters into string
        temp = ''
        for field in mapped_fields:
            temp += field + ','
        
        parameters = 'fields=' + temp[:-1]

        # call API
        response = requests.get(f'{url}?{parameters}', headers=headers)
        
    elif method == 'post':

        url = data_dictionary['base_url'] + data_dictionary['endpoint_mapping'][endpoint]['endpoint']

        try:
            mapped_fields['author'] = 'urn:li:person:' + mapped_fields['author']
        except:
            pass
        
        # call API
        response = requests.post(f'{url}', headers=headers, json=mapped_fields)
    return response