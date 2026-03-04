
def get_text(soup):
    if not soup:
        return ""
    return soup.get_text(" ", strip=True).lower()
