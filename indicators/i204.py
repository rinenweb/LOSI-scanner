CONFIG = {
    "name": "Mobile device accessibility",
    "description": "The portal displays and works well when accessed through a mobile device (e.g., smartphone or tablet)."
}
def run(soup, url, **kwargs):
    if not soup:
        return 0, None

    meta = soup.find("meta", attrs={"name":"viewport"})

    if meta:
        return 1, "viewport meta tag"

    return 0, None
