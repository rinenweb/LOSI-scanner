import requests
import unicodedata
from urllib.parse import urlparse


HEADERS = {
    "User-Agent": "LOSI-Portal-Scanner"
}


def same_domain(url1, url2):
    try:
        return urlparse(url1).netloc == urlparse(url2).netloc
    except Exception:
        return False


def fetch_url(url, timeout=10):
    """
    Fetch a URL, follow redirects, and block cross-domain redirects.
    Returns a dict with:
      original_url, final_url, status, redirected, response, (optional) error
    """
    try:
        r = requests.get(
            url,
            headers=HEADERS,
            timeout=timeout,
            allow_redirects=True,
        )

        final_url = r.url
        redirected = len(r.history) > 0

        # block cross-domain redirects (e.g. portal -> facebook)
        if redirected and not same_domain(url, final_url):
            return {
                "original_url": url,
                "final_url": final_url,
                "status": "blocked_redirect",
                "redirected": True,
                "response": None,
            }

        return {
            "original_url": url,
            "final_url": final_url,
            "status": r.status_code,
            "redirected": redirected,
            "response": r,
        }

    except Exception as e:
        return {
            "original_url": url,
            "final_url": None,
            "status": "error",
            "redirected": False,
            "response": None,
            "error": str(e),
        }


def normalize_text(text: str) -> str:
    """
    Case-insensitive + accent-insensitive normalization.
    Works well for Greek (and generally any accented Latin script).
    """
    if not text:
        return ""

    # lower
    text = text.lower()

    # strip diacritics (τόνοι)
    text = "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )

    # normalize whitespace a bit
    return " ".join(text.split())


def get_text(soup) -> str:
    if not soup:
        return ""
    return normalize_text(soup.get_text(" ", strip=True))import requests
from urllib.parse import urlparse


HEADERS = {
    "User-Agent": "LOSI-Portal-Scanner"
}


def same_domain(url1, url2):

    try:
        return urlparse(url1).netloc == urlparse(url2).netloc
    except:
        return False


def fetch_url(url, timeout=10):

    try:

        r = requests.get(
            url,
            headers=HEADERS,
            timeout=timeout,
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
