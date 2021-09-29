import requests

def create_header(access_token):
    '''
    Prepare headers to attach to request.
    '''

    headers = {
    'Authorization': f'Bearer {access_token}'
    }
    return headers

def call_api(access_token, data_dictionary, method, endpoint, path, mapped_fields, id):
    # assemble the url without the parameters
    url = data_dictionary['base_url'] + data_dictionary['endpoint_mapping'][endpoint]['endpoint']
    if id != None:
        url += '/' + id
    if path != None:
        url += '/' + data_dictionary['endpoint_mapping'][endpoint]['paths'][path]['path']
    
    # remove possible duplicates
    mapped_fields = list(dict.fromkeys(mapped_fields))

    # concatenate parameters into string
    temp = ''
    for field in mapped_fields:
        temp += field + ','
    
    parameters = 'fields=' + temp[:-1]

    headers = create_header(access_token)

    # call API
    response = requests.get(f'{url}?{parameters}', headers=headers)

    return response