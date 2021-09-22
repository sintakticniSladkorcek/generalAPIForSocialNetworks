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


def convert_id_to_urn(id, endpoint):
    if endpoint == 'ugcPosts':
        id = f'urn:li:person:{id}'
    elif endpoint == 'socialActions':
        id = f"urn:li:share:{id}"
    return id


def call_api(access_token, data_dictionary, method, endpoint, path, mapped_fields, id):
    specific_endpoint = data_dictionary['endpoint_mapping'][endpoint]['endpoint']

    url = data_dictionary['base_url'] + specific_endpoint
    if id != None:
        id = convert_id_to_urn(id, specific_endpoint)
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

        if specific_endpoint == 'ugcPosts':
            url = data_dictionary['base_url'] + specific_endpoint

        try:
            mapped_fields['author'] = 'urn:li:person:' + mapped_fields['author']
        except:
            pass

        try:
            mapped_fields['actor'] = "urn:li:person:" + mapped_fields['actor']
        except:
            pass

        try:
            mapped_fields['object'] = "urn:li:share:" + mapped_fields['object']
        except:
            pass
        
        # call API
        response = requests.post(f'{url}', headers=headers, json=mapped_fields)

    return response


# https://api.linkedin.com/v2/socialActions/urn:li:share:6846571668672970753/likes
# {'actor': 'urn:li:person:cAnJ0yFHOX', 'object': 'urn:li:share:6846571668672970753'}

# https://api.linkedin.com/v2/socialActions/urn:li:share:6846571668672970753/likes
# {"actor": "urn:li:person:cAnJ0yFHOX", "object": "urn:li:share:6846571668672970753"}