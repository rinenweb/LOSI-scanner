CONFIG = {
    "name": "Internal search mechanism",
    "description": "A search bar on the main web page of the municipal government portal."
}
def run(soup, url, **kwargs):
    if not soup:
        return 0, None

    if soup.find("input", {"type":"search"}):
        return 1, "input[type=search]"

    if soup.find("form", {"role":"search"}):
        return 1, "form[role=search]"

    return 0, None
