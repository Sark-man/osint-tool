# whois_lookup.py

"""
Simplle WHOIS lookup wrapper.
"""
import whois

def domain_lookup(domain: str) -> dict:
    """
    Return WHOIS info for a given domain.
    """
    try:
        info = whois.whois(domain)
        return{
            "domain_name": info.get("domain_name"),
            "registrar": info.get("registrar"),
            "name_servers": info.get("name_servers"),
            "creation_date": info.get("creation_date"),
            "expiration_date": info.get("expiration_date"),
            "emails": info.get("emails")
        }
    except Exception as e:
        return {"error": f"WHOIS error: {e}"}