# streamlit_app.py
import streamlit as st
import pandas as pd
import os

# imports matching your module function names
from modules.whois_lookup import domain_lookup
from modules.social_scraper import check_username
from modules.shodan_lookup import shodan_lookup
from modules.hibp_lookup import check_account, check_password

st.set_page_config(page_title="OSINT Automation Tool", layout="wide")
st.title("🕵️ OSINT Automation Tool")
st.write("Interactive web UI for WHOIS, username footprinting, Shodan and HIBP checks.")

st.sidebar.markdown("### Actions")
option = st.sidebar.selectbox(
    "Choose an action:",
    ["WHOIS Lookup", "Username Footprinting", "Shodan Lookup", "HIBP Account Check", "HIBP Password Check"]
)

def show_result(result):
    if isinstance(result, dict) and "error" in result:
        st.error(result["error"])
    else:
        st.json(result)

if option == "WHOIS Lookup":
    domain = st.text_input("Enter a domain (e.g., example.com):")
    if st.button("Run WHOIS"):
        if domain:
            with st.spinner("Running WHOIS..."):
                res = domain_lookup(domain)
            show_result(res)
            if isinstance(res, dict):
                df = pd.json_normalize(res)
                st.download_button("Download WHOIS as CSV", df.to_csv(index=False), file_name=f"{domain}_whois.csv")

elif option == "Username Footprinting":
    username = st.text_input("Enter a username:")
    delay = st.slider("Delay between requests (seconds)", 0.1, 2.0, 0.5)
    if st.button("Check Username"):
        if username:
            with st.spinner("Checking platforms..."):
                res = check_username(username, delay)
            show_result(res)
            if isinstance(res, dict):
                rows = [{"platform": k, "status": v} for k, v in res.items()]
                df = pd.DataFrame(rows)
                st.dataframe(df)
                st.download_button("Download results CSV", df.to_csv(index=False), file_name=f"{username}_footprint.csv")

elif option == "Shodan Lookup":
    ip = st.text_input("Enter an IP address or domain (e.g., 8.8.8.8):")
    if st.button("Run Shodan"):
        if ip:
            # ensure SHODAN_API_KEY is set
            if not os.getenv("SHODAN_API_KEY"):
                st.warning("SHODAN_API_KEY not set. Set it as an env var before running.")
            else:
                with st.spinner("Querying Shodan..."):
                    res = shodan_lookup(ip)
                show_result(res)
                if isinstance(res, dict) and "ip" in res:
                    df = pd.json_normalize(res)
                    st.download_button("Download Shodan CSV", df.to_csv(index=False), file_name=f"{ip}_shodan.csv")

elif option == "HIBP Account Check":
    account = st.text_input("Enter an email or username:")
    if st.button("Check Breaches"):
        if account:
            if not os.getenv("HIBP_API_KEY"):
                st.warning("HIBP_API_KEY not set. This endpoint requires a paid HIBP API key.")
            else:
                with st.spinner("Checking HIBP..."):
                    res = check_account(account)
                show_result(res)
                # If breaches returned, offer JSON download
                if isinstance(res, dict) and "breaches" in res and res["breaches"]:
                    import json
                    st.download_button(
                        "Download breaches JSON",
                        json.dumps(res["breaches"], indent=2),
                        file_name=f"{account}_breaches.json"
                    )

elif option == "HIBP Password Check":
    password = st.text_input("Enter a password:", type="password")
    if st.button("Check Password"):
        if password:
            with st.spinner("Checking password (k-anonymity)..."):
                res = check_password(password)
            show_result(res)
            # Do NOT store or export plaintext passwords
            if isinstance(res, dict):
                st.write("Note: plaintext passwords are not stored or exported by this app.")
