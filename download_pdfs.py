import httpx
import os
from datetime import datetime, timedelta

def get_next_month_ym():
    today = datetime.today()
    next_month = today.replace(day=28) + timedelta(days=4)  # ensures we get into next month
    ym = next_month.strftime("%y%m")
    return ym

def generate_filenames():
    ym = get_next_month_ym()
    filenames = []

    # 'A' cruise codes: 01-12 + 02A, 03A
    for i in range(1, 13):
        suffix = f"{i:02d}"
        filenames.append(f"{ym}A{suffix}")
    filenames.append(f"{ym}A02A")
    filenames.append(f"{ym}A03A")

    # 'C' cruise codes: 01-09 + 02A, 03A
    for i in range(1, 10):
        suffix = f"{i:02d}"
        filenames.append(f"{ym}C{suffix}")
    filenames.append(f"{ym}C02A")
    filenames.append(f"{ym}C03A")

    return filenames

def download_pdf(url, path):
    print(f"🌐 Requesting: {url}")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/pdf",
        "Referer": "https://www.royalcaribbean.com/",
    }

    try:
        with httpx.Client(follow_redirects=True, timeout=30) as client:
            response = client.get(url, headers=headers)

        print(f"🔍 Status Code: {response.status_code}")
        print(f"🔍 Final URL: {response.url}")
        print(f"🔍 Content-Type: {response.headers.get('Content-Type', '')}")

        if response.status_code == 200 and 'application/pdf' in response.headers.get('Content-Type', ''):
            with open(path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Downloaded: {os.path.basename(path)}")
        else:
            print(f"❌ Skipped (Not a PDF or unexpected response): {os.path.basename(path)}")

    except httpx.ReadTimeout:
        print(f"⏱️ Timeout error for {url}")
    except httpx.RequestError as e:
        print(f"⚠️ Error downloading {os.path.basename(path)}: {e}")

def download_all_pdfs():
    base_url = "https://www.royalcaribbean.com/content/dam/royal/resources/pdf/casino/offers/"
    pdf_dir = "pdfs"
    os.makedirs(pdf_dir, exist_ok=True)

    filenames = generate_filenames()

    for name in filenames:
        url = f"{base_url}{name}.pdf"
        file_path = os.path.join(pdf_dir, f"{name}.pdf")
        download_pdf(url, file_path)

if __name__ == "__main__":
    download_all_pdfs()
