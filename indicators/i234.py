CONFIG = {
    "type": "keyword",
    "keywords_default": [
        "privacy policy",
        "πολιτική απορρήτου"
    ],
    "case_insensitive": True,
    "accent_insensitive": True
}
from scanner.html_utils import normalize_text
def run(soup, url, keywords=None, **kwargs):
    if not soup:
        return 0, None
    if not keywords:
        keywords = CONFIG["keywords_default"]

    keywords = [normalize_text(k) for k in keywords]

    for a in soup.find_all("a", href=True):
        text = normalize_text(a.text)
        for kw in keywords:
            if kw in text:
                return 1, a["href"]
    return 0, None
