# modules/shodan_lookup.py
import os
import requests

def shodan_lookup(ip: str) -> dict:
    try:
        # Try Streamlit secrets first
        import streamlit as st
        api_key = st.secrets.get("SHODAN_API_KEY", None)
    except ImportError:
        # Fallback if running locally
        api_key = os.getenv("SHODAN_API_KEY")

    if not api_key:
        return {"error": "Missing SHODAN_API_KEY (set as env var locally or in Streamlit secrets)"}

    url = f"https://api.shodan.io/shodan/host/{ip}?key={api_key}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "ip": data.get("ip_str"),
                "organization": data.get("org"),
                "os": data.get("os"),
                "ports": data.get("ports"),
                "hostnames": data.get("hostnames"),
                "country": data.get("country_name")
            }
        return {"error": f"Shodan error {resp.status_code}: {resp.text}"}
    except Exception as e:
        return {"error": str(e)}
