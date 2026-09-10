from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By

def _driver():
    errors = []
    try:
        opts = ChromeOptions()
        opts.add_argument("--headless=new")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--no-sandbox")
        return webdriver.Chrome(options=opts)
    except Exception as e:
        errors.append(str(e))
    try:
        opts = EdgeOptions()
        opts.add_argument("--headless=new")
        opts.add_argument("--disable-gpu")
        return webdriver.Edge(options=opts)
    except Exception as e:
        errors.append(str(e))
    raise RuntimeError("No supported browser could be started. Install Google Chrome or Microsoft Edge.")

def fetch_webpage(url):
    driver = _driver()
    try:
        driver.get(url)
        body = driver.find_element(By.TAG_NAME, "body")
        return {"status": "success", "title": driver.title, "url": driver.current_url,
                "text": body.text[:30000]}
    finally:
        driver.quit()

def web_search(query, limit=5):
    driver = _driver()
    try:
        driver.get("https://www.google.com/search?q=" + quote(query))
        links = driver.find_elements(By.CSS_SELECTOR, "a")
        results = []
        seen = set()
        for a in links:
            href = a.get_attribute("href")
            text = (a.text or "").strip()
            if href and text and href.startswith("http") and "google.com" not in href:
                if href not in seen:
                    seen.add(href)
                    results.append({"title": text[:300], "url": href})
            if len(results) >= limit:
                break
        return {"status": "success", "query": query, "results": results}
    finally:
        driver.quit()
