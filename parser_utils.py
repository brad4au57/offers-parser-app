import pdfplumber
import pandas as pd
import json

NORMALIZED_COLUMNS = [
    "Offer Code",
    "Ship",
    "Departure Port",
    "Sail Date",
    "Itinerary",
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

                for col in NORMALIZED_COLUMNS:
                    if col not in df.columns:
                        df[col] = ""

                df = df[NORMALIZED_COLUMNS]
                all_data.append(df)

    if not all_data:
        print("❌ No table data found in PDF.")
        return

    combined = pd.concat(all_data, ignore_index=True)

    cleaned = []
    for row in combined.to_dict(orient="records"):
        cleaned_row = {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
        cleaned.append(cleaned_row)

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    print(f"✅ Table data extracted and saved to {output_json_path}")
