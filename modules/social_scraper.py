# social_scraper.py
"""
Check presence of a username across platforms by HTTP status.
"""

import requests
from time import sleep

PLATFORMS = {
    "GitHub": "https://github.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "LinkedIn": "https://www.linkedin.com/in/{}"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; OSINTTool/1.0; +https://github.com/yourusername)"
}

def check_username(username: str, delay: float = 0.5) -> dict:
    """
    For each platform, check if username exists.
    """
    results = {}
    for name, url_template in PLATFORMS.items():
        url = url_template.format(username)
        try:
            resp = requests.get(url, headers=HEADERS, timeout=8)
            if resp.status_code == 200:
                results[name] = "Found"
            elif resp.status_code == 404:
                results[name] = "Not Found"
            else:
                results[name] = f"Status {resp.status_code}"
        except requests.RequestException as e:
            results[name] = f"Error: {e}"
        sleep(delay)  # avoid hammering servers
    return results
