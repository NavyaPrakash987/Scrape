import requests

api_key = "AIzaSyDl03tWvm2zA87BRaslbKuaJDWbohZ1_Ws"

url = "https://www.searchapi.io/api/v1/search"
params = {
  "engine": "google",
  "q": "npci",
  "api_key" : api_key
}

response = requests.get(url, params=params)
print(response.text)
