import pandas as pd
from typing import Dict, List, Generator
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV_PATH = os.path.join(BASE_DIR, "main.csv")


def load_csv_file(file_path: str = DEFAULT_CSV_PATH) -> Dict[str, List[Dict]]:
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found at: {file_path}")

    try:
       
        df = pd.read_csv(file_path, encoding="utf-8", on_bad_lines="skip")
    except Exception:
      
        try:
            df = pd.read_csv(file_path, delimiter=";", encoding="utf-8", on_bad_lines="skip")
        except Exception:
            df = pd.read_csv(file_path, delimiter="\t", encoding="utf-8", on_bad_lines="skip")

    all_results = {"CSV": df.fillna("").to_dict(orient="records")}
    return all_results


def row_to_text_generator(all_results: dict) -> Generator[str, None, None]:
    for table_name, rows in all_results.items():
        yield f"\n=== {table_name} ==="
        for row in rows:
            row_str = " | ".join([f"{k}: {v}" for k, v in row.items() if str(v).strip()])
            if row_str.strip():
                yield row_str


def row_to_text(all_results: dict) -> str:
    return "\n".join(row_to_text_generator(all_results))


