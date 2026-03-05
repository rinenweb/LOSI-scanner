import requests
import unicodedata
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def same_domain(url1, url2):
    try:
        return urlparse(url1).netloc == urlparse(url2).netloc
    except Exception:
        return False

def fetch_url(url, timeout=10):

    try:
        r = requests.get(
            url,
            headers=HEADERS,
            timeout=10,
            allow_redirects=True
        )

        final_url = r.url
        redirected = len(r.history) > 0

        # block cross-domain redirects
        if redirected and not same_domain(url, final_url):

            return {
                "original_url": url,
                "final_url": final_url,
                "status": "blocked_redirect",
                "redirected": True,
                "response": None
            }

        return {
            "original_url": url,
            "final_url": final_url,
            "status": r.status_code,
            "redirected": redirected,
            "response": r
        }

    except Exception as e:

        return {
            "original_url": url,
            "final_url": None,
            "status": "error",
            "redirected": False,
            "response": None,
            "error": str(e)
        }

def normalize_text(text: str) -> str:

    if not text:
        return ""

    text = text.lower()

    text = "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )

    return " ".join(text.split())

def get_text(soup):

    if not soup:
        return ""

    return normalize_text(soup.get_text(" ", strip=True))
