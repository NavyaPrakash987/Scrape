import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import os

json_data = []
visited = set()
# to_visit = ["https://www.theshineapp.com/"]
to_visit = ["https://example.com"]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def is_internal(url, base_netloc):
    return urlparse(url).netloc == base_netloc or urlparse(url).netloc == ''

while to_visit:
    url = to_visit.pop(0)
    if url in visited:
        continue

    try:
        print(f"Scraping: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        visited.add(url)

        # Save or process page content to html
        # with open(f"pages/{urlparse(url).path.replace('/', '_') or 'home'}.html", "w", encoding='utf-8') as f:
        #     f.write(response.text)


        page_text = soup.get_text(separator="\n", strip=True)
        json_data.append({
        "text": page_text,
        "metadata": {
            "source": url
            }})


        base_netloc = urlparse(url).netloc

        for link in soup.find_all("a", href=True):
            href = link["href"]
            full_url = urljoin(url, href)

            if is_internal(full_url, base_netloc) and full_url not in visited and full_url not in to_visit:
                to_visit.append(full_url)

        time.sleep(1)  # delay between requests
    except Exception as e:
        print(f"Failed: {url} — {e}")
# Save to JSON file
os.makedirs("data", exist_ok=True)
with open("data/npci_web_content.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

print("✅ Scraping complete. Data saved to data/npci_web_content.json")