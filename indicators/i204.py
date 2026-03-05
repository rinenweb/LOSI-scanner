CONFIG = {
    "name": "Mobile device accessibility",
    "description": "The portal displays and works well when accessed through a mobile device (e.g., smartphone or tablet)."
    "crawl": False
}
def run(pages, url, **kwargs):
    if not pages:
        return 0, None
    soup = pages[0]["soup"]
    meta = soup.find("meta", attrs={"name":"viewport"})

    if meta:
        return 1, pages[0]["url"]

    return 0, None
