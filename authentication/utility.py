import json

class Utility:

    def read_credentials(filename):
        with open(filename) as f:
            credentials = json.load(f)
        return credentials

    def save_token(filename, data):
        data = json.dumps(data, indent = 4) 
        with open(filename, 'w') as f: 
            f.write(data)