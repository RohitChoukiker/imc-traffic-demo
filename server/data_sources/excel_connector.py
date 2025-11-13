# import pandas as pd
# from typing import Dict, List, Generator
# import os

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DEFAULT_EXCEL_PATH = os.path.join(BASE_DIR, "synthetic_challan_data_indore.xlsx")


# def load_excel_file(file_path: str = DEFAULT_EXCEL_PATH) -> Dict[str, List[Dict]]:
   
#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"Excel file not found at: {file_path}")

#     excel_data = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")
#     all_results = {}
#     for sheet_name, df in excel_data.items():
#         all_results[sheet_name] = df.fillna("").to_dict(orient="records")
#     return all_results


# def row_to_text_generator(all_results: dict) -> Generator[str, None, None]:
    
#     for table_name, rows in all_results.items():
#         yield f"\n=== {table_name} ==="
#         for row in rows:
#             # Empty values skip
#             row_str = " | ".join([f"{k}: {v}" for k, v in row.items() if v])
#             if row_str.strip():
#                 yield row_str


# def row_to_text(all_results: dict) -> str:
    
#     return "\n".join(row_to_text_generator(all_results))

