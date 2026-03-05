from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from scanner.html_utils import fetch_url

def crawl_site(start_url, max_pages=10):

    visited = set()
    to_visit = [start_url]
    pages = []

    base_domain = urlparse(start_url).netloc

    while to_visit and len(pages) < max_pages:
        url = to_visit.pop(0)

        if url in visited:
            continue

        visited.add(url)
        result = fetch_url(url)

        if result["status"] != 200 or not result["response"]:
            continue

        html = result["response"].text
        soup = BeautifulSoup(html, "html.parser")

        pages.append({
            "url": url,
            "soup": soup
        })

        # συλλογή εσωτερικών links
        for a in soup.find_all("a", href=True):

            link = urljoin(url, a["href"])
            parsed = urlparse(link)

            if parsed.netloc != base_domain:
                continue

            clean = parsed.scheme + "://" + parsed.netloc + parsed.path

            if clean not in visited:
                to_visit.append(clean)
    return pages
