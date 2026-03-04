import requests
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
