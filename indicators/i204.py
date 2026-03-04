
def run(soup, url):
    if not soup:
        return 0, None

    meta = soup.find("meta", attrs={"name":"viewport"})

    if meta:
        return 1, "viewport meta tag"

    return 0, None
