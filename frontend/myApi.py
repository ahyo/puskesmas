import requests, json

def api_post(path='',data={},token=''):
    url = "http://127.0.0.1:8000/"+path
    body = json.dumps(data)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer '+token
    }
    response = requests.post(url, headers=headers, data=body, verify=False)
    return response.json()

def api_get(path='',data={},token=''):
    url = "http://127.0.0.1:8000/"+path
    body = json.dumps(data)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer '+token
    }
    response = requests.get(url, headers=headers, data=body, verify=False)
    return response.json()