# modules/request_utils.py
import time
import random
import requests


#proxy rotation
# proxies = {
#     "http": "http://123.123.123.123:8000",
#     "https": "https://123.123.123.123:8000",
# }
# requests.get(url, headers=headers, proxies=proxies)

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
]

def safe_get(url, headers=None, retries=3, timeout=10):
    headers = headers or {
        "User-Agent": random.choice(user_agents)
    }
    for i in range(retries):
        try:
            time.sleep(random.uniform(1, 3))
            return requests.get(url, headers=headers, timeout=timeout)
        except requests.RequestException:
            time.sleep(2)
    return None
