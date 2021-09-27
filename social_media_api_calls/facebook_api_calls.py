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
        # call API
        response = requests.post(f'{url}', json=mapped_fields, headers=headers)

    elif method == 'delete':
        # call API
        response = requests.post(f'{url}', headers=headers)

    # print(response.json())
    return response

