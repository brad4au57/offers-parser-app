import os
import sys
from parser_utils import extract_table_from_pdf

if __name__ == "__main__":
    pdf_folder = "pdfs"
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    def file_sort_key(filename):
        return os.path.splitext(filename)[0]

    pdf_files = sorted(
        [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")],
        key=file_sort_key
    )

    if not pdf_files:
        print("❌ No PDF files found.")
        sys.exit(1)

    print(f"📄 Found {len(pdf_files)} PDF file(s) to process.\n")

    for filename in pdf_files:
        input_path = os.path.join(pdf_folder, filename)
        output_path = os.path.join(output_folder, filename.replace(".pdf", ".json"))

        print(f"🔄 Processing: {filename}")
        extract_table_from_pdf(input_path, output_path)
        print()
