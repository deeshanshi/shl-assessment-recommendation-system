import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# -----------------------------
# Fetch duration from detail page
# -----------------------------
def fetch_duration(assessment):
    try:
        res = requests.get(assessment["url"], headers=HEADERS, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            text = soup.get_text(" ").lower()
            match = re.search(r'(\d+)\s*(min|minute)', text)
            if match:
                assessment["duration"] = int(match.group(1))
    except:
        pass
    return assessment


# -----------------------------
# Parse table rows
# -----------------------------
def parse_table(table):
    results = []
    rows = table.find_all("tr")[1:]

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue

        name_tag = cols[0].find("a")
        if not name_tag:
            continue

        name = name_tag.text.strip()
        url = BASE_URL + name_tag.get("href")

        remote_support = "Yes" if cols[1].find("span", class_="-yes") else "No"
        adaptive_support = "Yes" if cols[2].find("span", class_="-yes") else "No"

        keys = cols[3].find_all("span", class_="product-catalogue__key")
        test_type = [k.text.strip() for k in keys]

        results.append({
            "name": name,
            "url": url,
            "description": name,
            "duration": None,
            "remote_support": remote_support,
            "adaptive_support": adaptive_support,
            "test_type": test_type
        })

    return results


# -----------------------------
# Scrape ONLY Individual Tests
# -----------------------------
def scrape_individual_tests(max_pages=40):
    all_data = []

    for start in range(0, max_pages * 12, 12):
        url = f"{CATALOG_URL}?type=1&start={start}"
        print(f"🔍 Scraping: {url}")

        res = requests.get(url, headers=HEADERS)
        if res.status_code != 200:
            break

        soup = BeautifulSoup(res.text, "html.parser")
        table = soup.find("table")
        if not table:
            break

        page_data = parse_table(table)
        if not page_data:
            break

        all_data.extend(page_data)
        time.sleep(1)

    return all_data


# -----------------------------
# MAIN
# -----------------------------
def main():
    print("🚀 Scraping SHL Individual Test Solutions (ONLY)")
    data = scrape_individual_tests()

    print(f"✅ Collected {len(data)} assessments")

    print("⏳ Fetching duration info...")
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_duration, d) for d in data]
        for _ in as_completed(futures):
            pass

    df = pd.DataFrame(data)
    df.drop_duplicates(subset=["url"], inplace=True)

    df.to_csv("data/processed/shl_assessments.csv", index=False)
    print("📁 Saved → data/processed/shl_assessments.csv")


if __name__ == "__main__":
    main()

