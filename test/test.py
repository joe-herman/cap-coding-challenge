import requests
import json

APP_URL='http://cap-app:5000/'
STRINGINATE_URL=f'{APP_URL}stringinate'
STATS_URL=f'{APP_URL}stats'


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

def test_stats_ok():
  testStr = 'reallyPopularString'
  for i in range(10):
    requests.post(STRINGINATE_URL, data=json.dumps({'input': testStr}), headers=CONTENT_TYPE_JSON)

  r = requests.get(STATS_URL)
  assert r.status_code == 200, f'HTTP 200 expected from {STATS_URL} {r.text}'
  response = r.json()
  assert response['most_popular'] == testStr, f'Expected most_popular to match {testStr}'


def test_stats_long_string():
  # Create a long string
  longStr = ''.join(['a'] * 1000)
  requests.post(STRINGINATE_URL, data=json.dumps({'input': longStr}), headers=CONTENT_TYPE_JSON)
  r = requests.get(STATS_URL)
  assert r.status_code == 200, f'HTTP 200 expected from {STATS_URL} {r.text}'
  response = r.json()
  assert response['longest_input_received'] == longStr, f'Expected longest_input_received to match {longStr}'
