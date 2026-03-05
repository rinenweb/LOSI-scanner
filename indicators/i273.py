CONFIG = {
    "name": "Social networking features",
    "description": "Presence of links to social networking platforms such as Facebook, Twitter, YouTube or Instagram."
    "crawl": True,
}
SOCIAL = ["facebook.com","twitter.com","youtube.com","instagram.com","linkedin.com"]

def run(pages, url, **kwargs):

    for p in pages:
        soup = p["soup"]
        for a in soup.find_all("a", href=True):
            for s in SOCIAL:
                if s in a["href"]:
                    return 1, a["href"]
    return 0, None
