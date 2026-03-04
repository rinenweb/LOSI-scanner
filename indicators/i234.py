
def run(soup, url):
    if not soup:
        return 0, None

    for a in soup.find_all("a", href=True):
        if "privacy" in a.text.lower():
            return 1, a.get("href")

    return 0, None
