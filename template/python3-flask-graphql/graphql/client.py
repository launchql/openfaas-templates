from six.moves import urllib
import json

class GraphQLClient:
    def __init__(self, endpoint, headers):
        self.endpoint = endpoint
        if headers is None:
            self.headers = {}
        else:
            self.headers = headers

        self.headers = self.headers.update({'Accept': 'application/json',
                   'Content-Type': 'application/json'})

        self.token = None
        self.headername = None

    def execute(self, query, variables=None):
        return self._send(query, variables)

    def inject_token(self, token, headername='Authorization'):
        self.token = token
        self.headername = headername

    def _send(self, query, variables):
        data = {'query': query,
                'variables': variables}
        headers = self.headers
    
        if self.token is not None:
            headers[self.headername] = '{}'.format(self.token)

        req = urllib.request.Request(self.endpoint, json.dumps(data).encode('utf-8'), headers)

        try:
            response = urllib.request.urlopen(req)
            return response.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            print((e.read()))
            raise e
