CONFIG = {
    "name": "Internal search mechanism",
    "description": "A search bar or search functionality on the municipal government portal.",
    "crawl": True,
}


def run(pages, url, **kwargs):
    for p in pages:
        soup = p["soup"]

        if soup.find("input", {"type": "search"}):
            return 1, p["url"]

        if soup.find("form", {"role": "search"}):
            return 1, p["url"]

        for a in soup.find_all("a", href=True):
            href = (a.get("href") or "").lower()
            text = a.get_text(strip=True).lower()

            if "/search" in href or "search" in href:
                return 1, p["url"]

            if "αναζήτηση" in text:
                return 1, p["url"]

        if soup.find(class_="fa-search"):
            return 1, p["url"]

    return 0, None
