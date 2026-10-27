#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

HOST = "www.gerardbutlerofficial.com"
KEY = "8f4b6932b1234a90886a10de088b907c"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"

def get_urls_from_sitemap(sitemap_path="sitemap.xml"):
    urls = []
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        for url in root.findall("ns:url", namespace):
            loc = url.find("ns:loc", namespace)
            if loc is not None and loc.text:
                urls.append(loc.text.strip())
    except Exception as e:
        print(f"Error reading sitemap: {e}")
    return urls

def ping_indexnow(urls):
    if not urls:
        print("No URLs to submit.")
        return False
    
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        INDEXNOW_ENDPOINT,
        data=data,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "GerardButlerOfficial-IndexNow/1.0"
        }
    )
    
    print(f"Submitting {len(urls)} URLs to IndexNow ({INDEXNOW_ENDPOINT})...")
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            status = response.getcode()
            print(f"IndexNow submission successful! HTTP status code: {status}")
            return True
    except urllib.error.HTTPError as e:
        print(f"IndexNow HTTP Error: {e.code} - {e.reason}")
        # 200: OK, 202: Accepted (valid for IndexNow)
        if e.code in [200, 202]:
            return True
        return False
    except Exception as e:
        print(f"IndexNow network error: {e}")
        return False

if __name__ == "__main__":
    urls = get_urls_from_sitemap()
    if not urls:
        urls = ["https://www.gerardbutlerofficial.com/"]
    ping_indexnow(urls)
