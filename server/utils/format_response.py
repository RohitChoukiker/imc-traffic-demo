import pandas as pd

def format_response(results: list, query: str = None) -> str:
  
    if not results:
        return "Sorry, no challan records found for your query."

    # Agar ek hi record hai toh natural sentence banao
    if len(results) == 1:
        r = results[0]
        natural_text = (
            f"🚦 A challan of **₹{r.get('Amount', r.get('Fine', 'N/A'))}** "
            f"was issued in **{r.get('Challan Place', 'N/A')}** "
            f"on **{r.get('Challan Date', 'N/A')}** "
            f"for vehicle **{r.get('Vehicle Number', 'N/A')}**. "
            f"The offence was: **{r.get('Challan Remark', r.get('Offence', 'N/A'))}**."
        )
    else:
        natural_text = (
            f"📊 Found **{len(results)} challans** matching your query. "
            f"Here’s a summary of the offences:"
        )

    # Convert to DataFrame
    df = pd.DataFrame(results)

    # Priority columns
    priority_cols = [
        "District",
    "Circle",
    "Challan Number",
    "Challan Source",
    "DL Number",
    "Vehicle Number",
    "Challan Date",
    "Challan Place",
    "Imei",
    "Latitue Longtitue",
    "Challan Remark",
    "Challaning Officer Name",
    "Challaning OfficerID",
    "Challaning Officer Designation",
    "Violator Type",
    "Violator Name",
    "Violator Address",
    "Violator Contact",
    "Owner Name",
    "Driver Name",
    "Driver Address",
    "Driver Contact",
    "Vehicle Impound",
    "Vehicle Impound Place",
    "Impound Doc Type",
    "Impunded Document Nos",
    "Document Impound Place",
    "Challan Status",
    "Challan Amount",
    "Payment Date",
    "Payment Source",
    "Payment Cin No",
    "Receipt Number",
    "Current Registration Authority",
    "Vehicle Class",
    "Engine Number",
    "Chasis Number",
    "Maker Model",
    "Send To Court Date",
    "Court Name",
    "Court Receipt No",
    "Court Release Date",
    "Offences",
    "Amount",
    "Fine"
    ]

    
    cols_to_show = [c for c in priority_cols if c in df.columns]

    # Extra columns (jo priority list me nahi hain)
    extra_cols = [c for c in df.columns if c not in cols_to_show]

    # Final order = priority cols + extra cols
    final_cols = cols_to_show + extra_cols

    df = df[final_cols]

    # Markdown table
    table_md = df.to_markdown(index=False)

    return f"{natural_text}\n\n#### 📋 Challan Details\n{table_md}"
