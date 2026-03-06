CONFIG = {
    "name": "Navigability",
    "description": "A sitemap or index with a list of all the available pages within the website accessible to users.",
    "crawl": True,
}


def run(pages, url, **kwargs):

    keywords = [
        "sitemap",
        "site map",
        "site-map",
        "χάρτης",
        "χάρτης ιστότοπου",
        "χάρτης ιστοσελίδας"
    ]

    url_patterns = [
        "/sitemap",
        "/site-map",
        "sitemap.xml"
    ]

    for p in pages:
        soup = p["soup"]

        # 1. link rel="sitemap"
        if soup.find("link", {"rel": "sitemap"}):
            return 1, p["url"]

        # 2. anchor links
        for a in soup.find_all("a", href=True):

            href = (a.get("href") or "").lower()
            text = a.get_text(strip=True).lower()

            for k in keywords:
                if k in text:
                    return 1, p["url"]

            for pat in url_patterns:
                if pat in href:
                    return 1, p["url"]

        # 3. direct sitemap xml references
        for link in soup.find_all("link", href=True):
            href = link["href"].lower()
            if "sitemap" in href:
                return 1, p["url"]

    return 0, None
