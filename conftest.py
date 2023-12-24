import pytest
import requests

class Api:
    def __init__(self, address):
        self.address = address

    def post(self, path="/", params=None, data=None, json=None, headers={}):
        url = f"{self.address}{path}"
        headers['accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'
        return requests.post(url=url, params=params, data=data, json=json, headers=headers, timeout=30)

    def get(self, path="/", params=None, headers={}):
        url = f"{self.address}{path}"
        headers['accept'] = 'application/json'
        return requests.get(url=url, params=params, headers=headers, timeout=30)
    
    def put(self, path="/", params=None, data=None, json=None, headers={}):
        url = f"{self.address}{path}"
        headers['accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'
        return requests.put(url=url, params=params, data=data, json=json, headers=headers, timeout=30)
    
    def delete(self, path="/", params=None, headers={}):
        url = f"{self.address}{path}"
        headers['accept'] = 'application/json'
        return requests.delete(url=url, params=params, headers=headers, timeout=30)
    
    def head(self, path="/", params=None, headers={}):
        url = f"{self.address}{path}"
        return requests.head(url=url, params=params, headers=headers, timeout=30)
    
    def patch(self, path="/", params=None, data=None, json=None, headers={}):
        url = f"{self.address}{path}"
        headers['accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'
        return requests.patch(url=url, params=params, data=data, json=json, headers=headers, timeout=30)

@pytest.fixture
def api():
    return Api(address="https://petstore.swagger.io/v2/")