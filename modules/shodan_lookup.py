import shodan
import os

def shodan_lookup(ip_or_domain: str) -> dict:
    try:
        api_key = os.getenv("SHODAN_API_KEY")
        if not api_key:
            return {"error": "Missing SHODAN_API_KEY. Set it as an environment variable."}

        api = shodan.Shodan(api_key)
        host = api.host(ip_or_domain)

        return {
            "ip": host.get("ip_str"),
            "organization": host.get("org"),
            "os": host.get("os"),
            "ports": host.get("ports"),
            "hostnames": host.get("hostnames"),
            "country": host.get("country_name")
        }
    except Exception as e:
        return {"error": f"Shodan error: {e}"}
