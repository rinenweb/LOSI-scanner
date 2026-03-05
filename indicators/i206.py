CONFIG = {
    "name": "Internal search mechanism",
    "description": "A search bar on the main web page of the municipal government portal.",
    "crawl": True
}
def run(pages, url, **kwargs):
   for p in pages:
        soup = p["soup"]
        if soup.find("input", {"type": "search"}):
            return 1, p["url"]
        if soup.find("form", {"role": "search"}):
            return 1, p["url"]
    return 0, None
