# modules/hibp_lookup.py
import os
import requests
import hashlib
import time

HIBP_BASE = "https://haveibeenpwned.com/api/v3"
USER_AGENT = "OSINTTool/1.0 (https://github.com/Sark-man)"

def _get_hibp_api_key():
    try:
        import streamlit as st
        return st.secrets.get("HIBP_API_KEY", None)
    except ImportError:
        return os.getenv("HIBP_API_KEY")

def check_account(account: str) -> dict:
    api_key = _get_hibp_api_key()
    if not api_key:
        return {"error": "Missing HIBP_API_KEY (set as env var locally or in Streamlit secrets)"}

    headers = {
        "hibp-api-key": api_key,
        "user-agent": USER_AGENT,
        "Accept": "application/json"
    }

    time.sleep(1.6)  # Respect rate limit
    url = f"{HIBP_BASE}/breachedaccount/{account}"
    resp = requests.get(url, headers=headers, params={"truncateResponse": False}, timeout=10)

    if resp.status_code == 200:
        return {"breaches": resp.json()}
    elif resp.status_code == 404:
        return {"breaches": []}
    else:
        return {"error": f"HIBP error {resp.status_code}: {resp.text}"}

def check_password(password: str) -> dict:
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
    if resp.status_code != 200:
        return {"error": f"Range API error: {resp.status_code}"}

    for line in resp.text.splitlines():
        suf, cnt = line.split(":")
        if suf == suffix:
            return {"pwned": True, "count": int(cnt)}
    return {"pwned": False}
