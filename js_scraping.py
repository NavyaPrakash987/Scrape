from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json

url = "https://example.com"
# url = "https://www.npci.org.in"

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(url)

# Give the page some time to load and execute JavaScript
driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to load

html = driver.page_source
driver.quit()

soup = BeautifulSoup(html, "html.parser")
page_text = soup.get_text(separator="\n", strip=True)

json_data = [{"text": page_text, "metadata": {"source": url}}]

with open("shine_app_content.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

print("Content with JavaScript rendered saved to shine_app_content.json")