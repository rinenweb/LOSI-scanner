CONFIG = {
    "name": "Social networking features",
    "description": "Presence of links to social networking platforms such as Facebook, Twitter, YouTube or Instagram."
}
SOCIAL = ["facebook.com","twitter.com","youtube.com","instagram.com","linkedin.com"]

def run(soup, url, **kwargs):
    if not soup:
        return 0, None

    for a in soup.find_all("a", href=True):
        for s in SOCIAL:
            if s in a["href"]:
                return 1, a["href"]

    return 0, None
