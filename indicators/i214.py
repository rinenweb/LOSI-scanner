CONFIG = {
    "name": "Contact details",
    "description": "Evidence of a 'contact us' feature including phone numbers, email addresses, physical addresses or contact forms."
    "crawl": True
}
import re

def run(pages, url, **kwargs):
    for p in pages:
        text = p["soup"].get_text().lower()
        email = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+", text)
        phone = re.search(r"\+?[0-9][0-9\-\s]{7,}", text)
        if email:
            return 1, p["url"]
        if phone:
            return 1, p["url"]
    return 0, None
