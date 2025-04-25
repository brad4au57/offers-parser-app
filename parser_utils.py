import pdfplumber
import pandas as pd
import json
import re

NORMALIZED_COLUMNS = [
    "Offer Code",
    "Ship",
    "Departure Port",
    "Sail Date",
    "Nights",
    "Destination",
    "Stateroom Type",
    "Offer Type",
    "Next Cruise Bonus",
]

HEADER_PREFIX = ["Offer Code", "Ship", "Departure Port"]

TABLE_SETTINGS = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines",
    "snap_tolerance": 3,
    "join_tolerance": 3,
    "edge_min_length": 3,
    "min_words_vertical": 3,
    "min_words_horizontal": 3,
    "text_keep_blank_chars": True,
    "text_tolerance": 3,
    "intersection_tolerance": 3,
}


def clean_row(row):
    if hasattr(row, "tolist"):
        row = row.tolist()
    while row and (row[-1] is None or str(row[-1]).strip() == ""):
        row = row[:-1]
    return [str(cell).strip() if cell else "" for cell in row]

def clean_ship_name(name: str) -> str:
    if not isinstance(name, str):
        return ""
    # Remove common symbols like ®, ™, ©
    return re.sub(r"[®™©]", "", name).strip()

def parse_itinerary(value):
    if not value or "Night" not in value:
        return "", value
    parts = value.split("Night", 1)
    nights = parts[0].strip()
    destination = parts[1].strip()
    return nights, destination


def extract_table_from_pdf(pdf_path, output_json_path):
    all_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            print(f"Reading page {i + 1}...")
            tables = page.extract_tables(TABLE_SETTINGS)

            for table_index, table in enumerate(tables):
                table = [clean_row(row) for row in table if any(cell and str(cell).strip() for cell in row)]

                header_index = None
                for idx, row in enumerate(table):
                    first_3 = [cell.lower() for cell in row[:3]]
                    if first_3 == [col.lower() for col in HEADER_PREFIX]:
                        header_index = idx
                        break

                if header_index is None:
                    print(f"⚠️ No header found in table {table_index + 1} on page {i + 1}")
                    continue

                header_row = table[header_index]
                data_rows = table[header_index + 1:]
                df = pd.DataFrame(data_rows)

                if df.shape[1] > len(header_row):
                    df = df.iloc[:, :len(header_row)]
                elif df.shape[1] < len(header_row):
                    print(f"⚠️ Row mismatch after header on page {i + 1}")
                    continue

                try:
                    df.columns = header_row
                except Exception as e:
                    print(f"⚠️ Could not assign headers on page {i + 1}: {e}")
                    continue

                # Handle column variation
                if "Next Cruise Bonus Stateroom Type" in df.columns:
                    df.rename(columns={"Next Cruise Bonus Stateroom Type": "Stateroom Type"}, inplace=True)
                    df["Next Cruise Bonus"] = None  # Use None as placeholder

                for col in ["Stateroom Type", "Next Cruise Bonus"]:
                    if col not in df.columns:
                        df[col] = ""

                # Now transform rows
                records = []
                for _, row in df.iterrows():
                    itinerary = row.get("Itinerary", "")
                    nights, destination = parse_itinerary(itinerary)

                    record = {
                        "Offer Code": row.get("Offer Code", ""),
                        "Ship": clean_ship_name(row.get("Ship", "")),
                        "Departure Port": row.get("Departure Port", ""),
                        "Sail Date": row.get("Sail Date", ""),
                        "Nights": nights,
                        "Destination": destination,
                        "Stateroom Type": row.get("Stateroom Type", ""),
                        "Offer Type": row.get("Offer Type", ""),
                        "Next Cruise Bonus": row.get("Next Cruise Bonus", None),
                    }
                    records.append(record)

                all_data.extend(records)

    if not all_data:
        print("❌ No table data found in PDF.")
        return

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Table data extracted and saved to {output_json_path}")
