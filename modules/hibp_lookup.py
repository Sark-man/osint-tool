import os
import requests
import hashlib
import time

HIBP_BASE = "https://haveibeenpwned.com/api/v3"
USER_AGENT = "OSINTTool/1.0 (https://github.com/Sark-man)"

def check_account(account: str) -> dict:
    """
    Check if an email/username has been exposed in known breaches (requires API key).
    """
    api_key = os.getenv("HIBP_API_KEY")
    if not api_key:
        return {"error": "Missing HIBP_API_KEY environment variable."}

    headers = {
        "hibp-api-key": api_key,
        "user-agent": USER_AGENT,
        "Accept": "application/json"
    }
    # Respect HIBP rate limit
    time.sleep(1.6)

    url = f"{HIBP_BASE}/breachedaccount/{account}"
    params = {"truncateResponse": False}
    resp = requests.get(url, headers=headers, params=params, timeout=10)

    if resp.status_code == 200:
        return {"breaches": resp.json()}
    elif resp.status_code == 404:
        return {"breaches": []}  # not found
    else:
        return {"error": f"HIBP error {resp.status_code}: {resp.text}"}

def check_password(password: str) -> dict:
    """
    Check if a password has been seen in breaches using k-anonymity (no API key required).
    """
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
