import requests, json

def api_call(path='',data={},token=''):
    url = "http://127.0.0.1:5000/"+path
    body = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=body, verify=False)
    return response.json()