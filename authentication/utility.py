import json

class Utility:

    def read_credentials(filename):
        with open(filename) as f:
            credentials = json.load(f)
        return credentials