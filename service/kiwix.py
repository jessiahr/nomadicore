import feedparser
import time
import json
import os

BASE_URL = "https://demo.library.kiwix.org/catalog/v2/entries?lang=eng"
ITEMS_PER_PAGE = 10  
ZIMS_STORE_PATH = "./data/kiwix"
def _fetch_zim_entries(start_index):
    url = f"{BASE_URL}&start={start_index}"
    feed = feedparser.parse(url)
    zim_list = []

    for entry in feed.entries:
        title = entry.title
        summary = entry.get("summary", "")
        zim_url = None
        for link in entry.links:
            if link.get("type") == "application/x-zim":
                zim_url = link.href.replace(".meta4", "")
        if zim_url:
            zim_list.append({
                "title": title,
                "summary": summary,
                "zim_url": zim_url,
            })

    total = int(feed.feed.get("totalresults", 0))
    return zim_list, total
def _maybe_log(log_callback, message):
    if log_callback:
        log_callback(message)
    print(message)
def _zim_index_path():
    if not os.path.exists(ZIMS_STORE_PATH):
        os.makedirs(ZIMS_STORE_PATH)
    return os.path.join(ZIMS_STORE_PATH, "zims.json")
def get_zim_index():
    try:
        with open(_zim_index_path(), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("ZIM index file not found. Please update the index.")
        return []
def kiwix_library_path():
    return os.path.join(ZIMS_STORE_PATH, "library")

def update_zim_index(log_callback=None):
    all_zims = []
    start_index = 0
    _maybe_log(log_callback, f"Fetching ZIM entries from {BASE_URL}...")
    while True:
        _maybe_log(log_callback, f"Fetching ZIM entries [{start_index} to {start_index + ITEMS_PER_PAGE}]")
        entries, total = _fetch_zim_entries(start_index)
        if not entries:
            _maybe_log(log_callback, "No more entries found.")
            break
        all_zims.extend(entries)
        start_index += ITEMS_PER_PAGE
        if start_index >= total:
            _maybe_log(log_callback, "Reached the end of entries.")
            break
        time.sleep(0.5)  # Be polite

    with open(_zim_index_path(), "w") as f:
        json.dump(all_zims, f, indent=4)
    _maybe_log(log_callback, f"ZIM index updated. Total ZIMs: {len(all_zims)}")
    return all_zims
