import requests


def call_api(access_token, data_dictionary, method, endpoint, path, mapped_fields, id):

    # assemble the url without the parameters
    url = data_dictionary['base_url'] + data_dictionary['endpoint_mapping'][endpoint]['endpoint']
    if id != None:
        url += '/' + id
    if path != None:
        url += '/' + data_dictionary['endpoint_mapping'][endpoint]['paths'][path]['path']
    
    
    if method == 'get':
        # prepare parameters
        parameters = 'fields=' + mapped_fields

        # call API
        # if mapped_fields == '':
        #     response = requests.get(f'{url}?&access_token={access_token}')
        # else:
        response = requests.get(f'{url}?{parameters}&access_token={access_token}')

    elif method == 'post':
        # prepare parameters
        parameters = ''
        for field_name in mapped_fields:
            parameters += field_name + '=' + str(mapped_fields[field_name]) + '&'
        parameters = parameters[:-1]

        # call API
        response = requests.post(f'{url}?{parameters}&access_token={access_token}')

    elif method == 'delete':
        response = None # TODO

    print(response.json())
    return response

