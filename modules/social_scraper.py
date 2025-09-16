# social_scraper.py
"""
Check presence of a username across platforms by HTTP status.
"""

import requests
import time
from time import sleep

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

PLATFORMS = {
    "GitHub": "https://github.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "LinkedIn": "https://www.linkedin.com/in/{}",
    "Snapchat" : "https://www.snapchat.com/add/{}",
    "Tiktok" : "https://www.tiktok.com/{}",

}


def check_username(username: str, delay: float = 0.5) -> dict:
    """
    For each platform, check if username exists.
    """
    results = {}
    for name, url_template in PLATFORMS.items():
        url = url_template.format(username)
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                results[name] = "Found"
            elif resp.status_code == 404:
                results[name] = "Not Found"
            elif resp.status_code == 429 and name == "Instagram":
                results[name] = "⚠️ Rate limited (try again later)"
            elif resp.status_code == 999 and name == "LinkedIn":
                results[name] = "⚠️ Restricted (LinkedIn blocks automated checks)"
            else:
                results[name] = f"Status {resp.status_code}"
        except requests.RequestException as e:
            results[name] = f"Error: {e}"

        time.sleep(1)  # avoid hammering servers
    return results
