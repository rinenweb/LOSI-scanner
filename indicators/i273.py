SOCIAL = ["facebook.com","twitter.com","youtube.com","instagram.com"]

def run(soup, url, **kwargs):
    if not soup:
        return 0, None

    for a in soup.find_all("a", href=True):
        for s in SOCIAL:
            if s in a["href"]:
                return 1, a["href"]

    return 0, None
