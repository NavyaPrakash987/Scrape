from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import tldextract
# from .request_utils import safe_get
import json
    # modules/request_utils.py
import time
import random
import requests

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


visited = set()
# base_url = "https://www.npci.org.in"
base_url = "https://example.com/"
domain = tldextract.extract(base_url).domain

def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and domain in parsed.netloc

def get_all_links(page_url):
    response = safe_get(page_url)
    if not response:
        return set()
    soup = BeautifulSoup(response.content, "html.parser")
    return {
        urljoin(page_url, tag["href"])
        for tag in soup.find_all("a", href=True)
        if is_valid_url(urljoin(page_url, tag["href"])) and urljoin(page_url, tag["href"]) not in visited
    }

def extract_clean_text(url):
    res = safe_get(url)
    if not res:
        return ""
    soup = BeautifulSoup(res.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]): tag.decompose()
    return soup.get_text(separator="\n").strip()

def crawl_website(start_url, max_pages=50):
    to_visit = [start_url]
    data = {}
    while to_visit and len(visited) < max_pages:
        current = to_visit.pop(0)
        if current in visited:
            continue
        visited.add(current)
        content = extract_clean_text(current)
        data[current] = content
        to_visit.extend(get_all_links(current))
    return data


site_data = crawl_website("https://example.com/", max_pages=30)
# logger.info("crawl NPCI site")
with open("data/site_data.json", "w") as f:
    json.dump(site_data, f, indent=2)




#proxy rotation
# proxies = {
#     "http": "http://123.123.123.123:8000",
#     "https": "https://123.123.123.123:8000",
# }
# requests.get(url, headers=headers, proxies=proxies)


