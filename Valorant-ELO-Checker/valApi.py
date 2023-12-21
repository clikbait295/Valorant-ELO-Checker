from requests.adapters import HTTPAdapter
from urllib3 import poolmanager
import requests
import ssl
import urllib.parse

class TLSAdapter(requests.adapters.HTTPAdapter):
  def init_poolmanager(self, connections, maxsize, block=False):
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    CIPHERS = [
      "ECDHE-ECDSA-CHACHA20-POLY1305",
      "ECDHE-RSA-CHACHA20-POLY1305",
      "ECDHE-ECDSA-AES128-GCM-SHA256",
      "ECDHE-RSA-AES128-GCM-SHA256",
      "ECDHE-ECDSA-AES256-GCM-SHA384",
      "ECDHE-RSA-AES256-GCM-SHA384",
      "ECDHE-ECDSA-AES128-SHA",
      "ECDHE-RSA-AES128-SHA",
      "ECDHE-ECDSA-AES256-SHA",
      "ECDHE-RSA-AES256-SHA",
      "AES128-GCM-SHA256",
      "AES256-GCM-SHA384",
      "AES128-SHA",
      "AES256-SHA",
      "DES-CBC3-SHA"
    ]
    ctx.set_ciphers(':'.join(CIPHERS))
    self.poolmanager = poolmanager.PoolManager(num_pools=connections, maxsize=maxsize, block=block, ssl_version=ssl.PROTOCOL_TLSv1_2, ssl_context=ctx)

class ValorantAPI(object):
  access_token = None
  cookies = None
  entitlements_token = None

  def __init__(self, username, password, region, client_ip):
    self.username = username
    self.password = password
    self.region = region
    self.client_ip = client_ip
    buildVersion = requests.get("https://valorant-api.com/v1/version").json()["data"]["buildVersion"]
    self.userAgent = f"ShooterGame/{buildVersion} Windows/10.0.22621.1.768.64bit"

    headers = {
      'Content-Type': 'application/json',
      'User-Agent': self.userAgent,
      'Accept': 'application/json, text/plain, */*'
    }

    self.session = requests.session()
    self.session.mount('https://', TLSAdapter())
    self.session.headers = headers

    self.get_cookies()

    self.access_token = self.get_access_token()

    self.entitlements_token = self.get_entitlements_token()

    self.user_info, self.game_name = self.get_user_info()

  def get_cookies(self):
    data = {
      'client_id': 'play-valorant-web-prod',
      'nonce': '1',
      'redirect_uri': 'https://playvalorant.com/opt_in',
      'response_type': 'token id_token',
      'scope': 'account openid'
    }
    headers = {
      'Content-Type': 'application/json',
      'User-Agent': self.userAgent,
      'Accept': 'application/json, text/plain, */*',
      'X-Forwarded-For': self.client_ip
    }
    self.session.post('https://auth.riotgames.com/api/v1/authorization', headers=headers, json=data)

  def get_access_token(self):
    data = {
      'type': 'auth',
      'username': self.username,
      'password': self.password
    }
    headers = {
      'Content-Type': 'application/json',
      'User-Agent': self.userAgent,
      'Accept': 'application/json, text/plain, */*',
      'X-Forwarded-For': self.client_ip
    }
    r = self.session.put('https://auth.riotgames.com/api/v1/authorization', headers=headers, json=data)

    uri = r.json()['response']['parameters']['uri']
    jsonUri = urllib.parse.parse_qs(uri)

    access_token = jsonUri['https://playvalorant.com/opt_in#access_token'][0]
    return access_token

  def get_entitlements_token(self):
    headers = {
      'Authorization': f'Bearer {self.access_token}',
      'Content-Type': 'application/json',
      'User-Agent': self.userAgent,
      'Accept': 'application/json, text/plain, */*',
      'X-Forwarded-For': self.client_ip
    }
    r = self.session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={})

    entitlements_token = r.json()['entitlements_token']

    return entitlements_token

  def get_user_info(self):
    headers = {
      'Authorization': f'Bearer {self.access_token}',
      'Content-Type': 'application/json',
      'User-Agent': self.userAgent,
      'Accept': 'application/json, text/plain, */*',
      'X-Forwarded-For': self.client_ip
    }

    r = self.session.post('https://auth.riotgames.com/userinfo', headers=headers, json={})
    jsonData = r.json()
    user_info = jsonData['sub']
    name = jsonData['acct']['game_name']
    tag  = jsonData['acct']['tag_line']
    game_name = name + ' #' +  tag

    return user_info, game_name

  def get_match_history(self):
    headers = {
      'Authorization': f'Bearer {self.access_token}',
      'Content-Type': 'application/json',
      'User-Agent': self.userAgent,
      'Accept': 'application/json, text/plain, */*',
      'X-Forwarded-For': self.client_ip,
      'X-Riot-Entitlements-JWT': f'{self.entitlements_token}',
      'X-Riot-ClientPlatform': "ewoJInBsYXRmb3JtVHlwZSI6ICJQQyIsCgkicGxhdGZvcm1PUyI6ICJXaW5kb3dzIiwKCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjIyNjIxLjEuNzY4LjY0Yml0IiwKCSJwbGF0Zm9ybUNoaXBzZXQiOiAiVW5rbm93biIKfQ==",
    }
    r = self.session.get(f'https://pd.{self.region}.a.pvp.net/mmr/v1/players/{self.user_info}/competitiveupdates?startIndex=0&endIndex=20', headers=headers)

    jsonData = r.json()

    return jsonData
