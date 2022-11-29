import requests
import json

#host = "http://192.168.50.227:8000/"
host = "http://localhost:8000/"
#host = "http://8.215.26.98:8000/"


def get_list_kunjungan():
    list_kunjungan = []
    kunjungan = api_get('kunjungan', None)

    if 'data' in kunjungan:
        list_kunjungan = kunjungan['data']
    return list_kunjungan


def api_post(path='', data={}, token=''):
    global host
    url = host+path
    body = json.dumps(data)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer '+token
    }
    response = requests.post(url, headers=headers, data=body, verify=False)
    return response.json()


def api_file(path='', files=[], token=''):
    global host
    url = host+path
    headers = {
        'Authorization': 'Bearer '+token
    }
    response = requests.post(url, headers=headers, files=files, verify=False)
    return response.json()


def api_get(path='', data={}, token=''):
    global host
    url = host+path
    body = json.dumps(data)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer '+token
    }
    response = requests.get(url, headers=headers, data=body, verify=False)
    return response.json()


def api_put(path='', data={}, token=''):
    global host
    url = host+path
    body = json.dumps(data)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer '+token
    }
    response = requests.put(url, headers=headers, data=body, verify=False)
    return response.json()
