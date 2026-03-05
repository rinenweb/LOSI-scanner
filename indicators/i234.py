CONFIG = {
    "name": "Privacy policy",
    "description": "Existence of a privacy policy or statement available on the municipal government portal.",
    "type": "keyword",
    "crawl": True,
    "keywords_default": [
        "privacy policy",
        "πολιτική απορρήτου"
    ],
    "case_insensitive": True,
    "accent_insensitive": True
}
from scanner.html_utils import normalize_text

def run(pages, url, keywords=None, **kwargs):

    if not keywords:
        keywords = CONFIG["keywords_default"]
    keywords = [normalize_text(k) for k in keywords]

    for p in pages:
        soup = p["soup"]
        for a in soup.find_all("a", href=True):
            text = normalize_text(a.text)
            for kw in keywords:
                if kw in text:
                    return 1, a["href"]
    return 0, None
