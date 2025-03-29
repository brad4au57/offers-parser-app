import pdfplumber
import pandas as pd
import os
import json
import sys

def extract_table_from_pdf(pdf_path, output_json_path):
    all_data = []
    headers = None

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            print(f"Reading page {i + 1}...")
            tables = page.extract_tables()

            for table in tables:
                df = pd.DataFrame(table)
                # Remove empty rows
                df = df.dropna(how='all')  
                 # Skip short or non-table sections
                if df.empty or df.shape[1] < 6: 
                    continue
                
                if headers is None:
                    # Assume first valid row with multiple non-null values is the header
                    first_row = df.iloc[0].dropna().tolist()
                    if len(first_row) >= 6:
                        headers = df.iloc[0].tolist()
                        df = df[1:]  # Remove header row from data
                    else:
                        continue
                else:
                    # If headers already defined, just use the whole table
                    pass

                df.columns = headers
                all_data.append(df)

    if not all_data:
        print("No table data found in PDF.")
        return
    
    combined = pd.concat(all_data, ignore_index=True)

    # Convert to list of dictionaries
    data_as_dict = combined.to_dict(orient="records")

    # Remove any entries where both the key and value are empty strings
    cleaned_data = []

    for row in data_as_dict:
        cleaned_row = {}
        for k, v in row.items():
            key = k.strip() if isinstance(k, str) else k
            value = v.strip() if isinstance(v, str) else v

            # Skip if the cleaned key is empty and the value is also empty
            if key == "" and (value == "" or value is None):
                continue

            cleaned_row[key] = value

        cleaned_data.append(cleaned_row)


    # Save to JSON
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Table data extracted and saved to {output_json_path}")

if __name__ == "__main__":# Remove empty rows
    pdf_folder = "pdfs"
    output_folder = "output"

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get all PDF files in the folder
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("❌ No PDF files found in the 'pdfs' folder.")
        sys.exit(1)

    print(f"📄 Found {len(pdf_files)} PDF file(s) to process.\n")

    for input_filename in pdf_files:
        input_pdf_path = os.path.join(pdf_folder, input_filename)
        output_filename = os.path.splitext(input_filename)[0] + ".json"
        output_json_path = os.path.join(output_folder, output_filename)

        print(f"🔄 Processing: {input_filename}")
        extract_table_from_pdf(input_pdf_path, output_json_path)
        print()