import requests


APP_URL='http://cap-app:5000/'

def test_app_ok():
  r = requests.get(APP_URL)
  assert r.status_code == 200, f'HTTP 200 expected from {APP_URL}'

