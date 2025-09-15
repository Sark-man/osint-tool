# 🕵️ OSINT Automation Tool

A lightweight Python tool for **Open Source Intelligence (OSINT)** tasks:  
- 🌐 WHOIS lookups on domains  
- 👤 Username footprinting across popular platforms  
- 📊 Exporting results to CSV for reporting  

This project is designed as a **student cybersecurity portfolio project** and is actively being expanded (Shodan & HaveIBeenPwned integrations coming soon 🚀).

---

## 📂 Features
- **WHOIS Lookup**: Get registrar, name servers, creation/expiry dates, and contact emails for a domain.  
- **Username Check**: Test if a username exists on GitHub, Twitter, Instagram, and LinkedIn.  
- **CSV Export**: Save results in a clean format for later analysis.  
- **CLI Interface**: Run like a real pentester’s tool with `--domain` or `--username`.  

---

## ⚡ Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/osint-tool.git
cd osint-tool
```

### 2. Create virtual environment & install dependencies

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell)**
```powershell
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 🚀 Usage

### WHOIS lookup
```bash
python main.py --domain google.com
```

Example output:
```json
{
  "domain_name": "GOOGLE.COM",
  "registrar": "MarkMonitor, Inc.",
  "name_servers": ["NS1.GOOGLE.COM", "NS2.GOOGLE.COM"],
  "creation_date": "1997-09-15",
  "expiration_date": "2028-09-14",
  "emails": ["abusecomplaints@markmonitor.com"]
}
```

---

### Username footprinting
```bash
python main.py --username torvalds --export torvalds.csv
```

Example console output:
```
[+] Checking username 'torvalds' across platforms ...
{'GitHub': 'Found', 'Twitter': 'Found', 'Instagram': 'Found', 'LinkedIn': 'Status 999'}
[+] Exported results to torvalds.csv
```

Example CSV (`torvalds.csv`):
```csv
type,target,platform,status
username,torvalds,GitHub,Found
username,torvalds,Twitter,Found
username,torvalds,Instagram,Found
username,torvalds,LinkedIn,Status 999
```

---

## 🛠️ Project Structure
```
osint-tool/
│── main.py
│── requirements.txt
│── modules/
│   ├── __init__.py
│   ├── whois_lookup.py
│   ├── social_scraper.py
│   └── utils.py
```

---

## 📌 Next Steps
Planned features:  
- 🔍 Shodan API integration (IP/domain intelligence)  
- 🔐 HaveIBeenPwned API integration (breach data check)  
- 🖥️ GUI dashboard for results visualization  

---

## ⚠️ Disclaimer
This tool is for **educational and ethical use only**.  
Do not use it to harass, stalk, or illegally investigate individuals or organizations. Always follow the law and obtain permission before running OSINT or security tests.

---

## 📜 License
This project is licensed under the [MIT License](LICENSE).
