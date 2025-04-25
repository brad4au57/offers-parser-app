import os
import httpx
from datetime import datetime, timedelta
from parser_utils import extract_table_from_pdf  # ✅ Import your shared parsing function

# ========== Step 1: Filename and URL Generation ==========

def get_next_month_ym():
    today = datetime.today()
    next_month = today.replace(day=28) + timedelta(days=4)
    return next_month.strftime("%y%m")

def generate_filenames():
    ym = get_next_month_ym()
    filenames = []

    # A-codes: 01-12 + 02A, 03A
    for i in range(1, 13):
        filenames.append(f"{ym}A{str(i).zfill(2)}")
    filenames += [f"{ym}A02A", f"{ym}A03A"]

    # C-codes: 01-09 + 02A, 03A
    for i in range(1, 10):
        filenames.append(f"{ym}C{str(i).zfill(2)}")
    filenames += [f"{ym}C02A", f"{ym}C03A"]

    return filenames

# ========== Step 2: Download PDFs ==========

def download_pdf(url, path):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/pdf",
        "Referer": "https://www.royalcaribbean.com/"
    }

    try:
        with httpx.Client(follow_redirects=True, timeout=30) as client:
            response = client.get(url, headers=headers)

        if response.status_code == 200 and 'application/pdf' in response.headers.get('Content-Type', ''):
            with open(path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Downloaded: {os.path.basename(path)}")
            return True
        else:
            print(f"❌ Skipped (Not a PDF or bad response): {os.path.basename(path)}")
            return False

    except Exception as e:
        print(f"⚠️ Error downloading {os.path.basename(path)}: {e}")
        return False

# ========== Step 3: Download + Parse All Files ==========

def run():
    base_url = "https://www.royalcaribbean.com/content/dam/royal/resources/pdf/casino/offers/"
    pdf_folder = "pdfs"
    json_folder = "output"

    os.makedirs(pdf_folder, exist_ok=True)
    os.makedirs(json_folder, exist_ok=True)

    filenames = generate_filenames()
    print(f"🔍 Processing {len(filenames)} file(s) for {get_next_month_ym()}...\n")

    for name in filenames:
        pdf_path = os.path.join(pdf_folder, f"{name}.pdf")
        json_path = os.path.join(json_folder, f"{name}.json")
        url = f"{base_url}{name}.pdf"

        if download_pdf(url, pdf_path):
            extract_table_from_pdf(pdf_path, json_path)

if __name__ == "__main__":
    run()
