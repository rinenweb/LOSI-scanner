CONFIG = {
    "name": "Internal search mechanism",
    "description": "Presence of a search bar or search functionality on the municipal government portal.",
    "crawl": True,
}


def run(pages, url, **kwargs):

    for p in pages:
        soup = p["soup"]

        # input type="search"
        if soup.find("input", {"type": "search"}):
            return 1, p["url"]

        # generic text inputs that behave like search fields
        for inp in soup.find_all("input", {"type": "text"}):
            placeholder = (inp.get("placeholder") or "").lower()
            name = (inp.get("name") or "").lower()
            iid = (inp.get("id") or "").lower()

            if "search" in placeholder or "αναζήτηση" in placeholder:
                return 1, p["url"]

            if "search" in name or "search" in iid:
                return 1, p["url"]

        # search forms
        if soup.find("form", {"role": "search"}):
            return 1, p["url"]

        for form in soup.find_all("form"):
            action = (form.get("action") or "").lower()
            if "search" in action:
                return 1, p["url"]

        # links to search pages
        for a in soup.find_all("a", href=True):
            href = (a.get("href") or "").lower()
            text = a.get_text(strip=True).lower()

            if "/search" in href or "search?" in href:
                return 1, p["url"]

            if "αναζήτηση" in text:
                return 1, p["url"]

        # search icons (eg. FontAwesome)
        if soup.find(class_="fa-search"):
            return 1, p["url"]

        if soup.find(class_="search"):
            return 1, p["url"]

        # javascript search triggers
        for el in soup.find_all(attrs={"onclick": True}):
            if "search" in el["onclick"].lower():
                return 1, p["url"]

        # elements with "search" in id or class (eg. overlays)
        for el in soup.find_all(True):

            el_id = (el.get("id") or "").lower()
            classes = el.get("class") or []
            class_str = " ".join(classes).lower()

            # refinement to not include cases like "research"
            if "search" in el_id or el_id.endswith("_search"):
                return 1, p["url"]

            for c in classes:
                c = c.lower()
                if c == "search" or c.startswith("search-") or c.endswith("-search"):
                    return 1, p["url"]

            if " search " in f" {class_str} ":
                return 1, p["url"]

    return 0, None
