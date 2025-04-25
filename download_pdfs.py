import os
from process_all_offers import generate_filenames, download_pdf, get_next_month_ym

def run_download_only():
    base_url = "https://www.royalcaribbean.com/content/dam/royal/resources/pdf/casino/offers/"
    pdf_dir = "pdfs"
    os.makedirs(pdf_dir, exist_ok=True)

    filenames = generate_filenames()
    print(f"📥 Downloading {len(filenames)} PDFs for {get_next_month_ym()}...\n")

    for name in filenames:
        url = f"{base_url}{name}.pdf"
        file_path = os.path.join(pdf_dir, f"{name}.pdf")
        download_pdf(url, file_path)

if __name__ == "__main__":
    run_download_only()
