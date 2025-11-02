import requests
from bs4 import BeautifulSoup
import time

def scrap_website(website):
    try:
        st_msg = f"🔍 Scraping {website} ..."
        print(st_msg)

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }

        response = requests.get(website, headers=headers, timeout=20)

        if "captcha" in response.text.lower() or "verify" in response.text.lower():
            print("⚠ Flipkart CAPTCHA or verification page detected.")
            return "<html><body><h3>CAPTCHA or bot protection detected. Try changing query or wait a bit.</h3></body></html>"

        response.raise_for_status()
        html = response.text
        print("✅ Page fetched successfully!")
        return html

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching website: {e}")
        return f"<html><body><h3>Error fetching website: {e}</h3></body></html>"


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style", "noscript"]):
        script_or_style.decompose()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    ]
