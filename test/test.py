import requests
import json

from werkzeug.datastructures import Headers

APP_URL='http://cap-app:5000/'
STRINGINATE_URL=f'{APP_URL}stringinate'

CONTENT_TYPE_JSON = {
  'Content-Type': 'application/json'
}

def test_app_ok():
  r = requests.get(APP_URL)
  assert r.status_code == 200, f'HTTP 200 expected from {APP_URL}'

def test_stringinate_ok():
  testStr = 'your-string-goes - here🦚'
  r = requests.post(STRINGINATE_URL, data=json.dumps({'input': testStr}), headers=CONTENT_TYPE_JSON)
  assert r.status_code == 200, f'HTTP 200 expected from {STRINGINATE_URL} {r.text}'
  response = r.json()
  assert response['input'] == testStr, f'Expected input to match sent string'
  assert response['length'] == len(testStr), f'Expected length to match sent string length'
  print(response)
  assert response['popularChar'] == 'r'



