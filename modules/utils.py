# utils.py
import pandas as pd
from typing import List, Dict

def export_to_csv(records: List[Dict], filename: str = "output.csv") -> None:
    """
    Export list of dicts to CSV file.
    """
    if not records:
        print("No records to export.")
        return
    df = pd.DataFrame(records)
    df.to_csv(filename, index=False)
    print(f"[+] Exported results to {filename}")
