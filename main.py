# main.py
"""
CLI for the OSINT Automation Tool
"""

import argparse
from modules.whois_lookup import domain_lookup
from modules.social_scraper import check_username
from modules.utils import export_to_csv
from modules.shodan_lookup import shodan_lookup
from modules.hibp_lookup import check_account, check_password

def cli():
    parser = argparse.ArgumentParser(description="OSINT Automation Tool (basic)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--domain", "-d", help="Domain to lookup")
    group.add_argument("--username", "-u", help="Username to check across platforms")
    group.add_argument("--shodan","-s", help ="IP or domain to lookup in Shodan")
    group.add_argument("--hibp-account", help="Check email/username against HIBP breaches")
    group.add_argument("--hibp-password", help="Check password via HIBP k-anonymity (not stored)")

    parser.add_argument("--export", "-e", help="CSV filename to export results", default=None)
    args = parser.parse_args()
   

    results = []

    if args.domain:
        print(f"[+] Running WHOIS lookup for {args.domain} ...")
        info = domain_lookup(args.domain)
        print(info)
        results = [{"type": "whois", "target": args.domain, **info}]

    if args.username:
        print(f"[+] Checking username '{args.username}' across platforms ...")
        info = check_username(args.username)
        print(info)
        for platform, status in info.items():
            results.append({"type": "username", "target": args.username, "platform": platform, "status": status})

    if args.export and results:
        export_to_csv(results, args.export)

    if args.shodan:
        print(f"[+] Running Shodan lookup for {args.shodan} ...")
        info = shodan_lookup(args.shodan)
        print(info)
        results = [{"type": "shodan", "target": args.shodan, **info}]

    if args.hibp_account:
        print(f"[+] Checking HIBP breaches for {args.hibp_account} ...")
        info = check_account(args.hibp_account)
        print(info)
        results = [{"type": "hibp_account", "target": args.hibp_account, **info}]

    if args.hibp_password:
        print("[+] Checking password against HIBP database ...")
        info = check_password(args.hibp_password)
        # Do NOT store plaintext password in results!
        results = [{"type": "hibp_password", "target": "<hidden>", **info}]
        print(info)


if __name__ == "__main__":
    cli()
