import re

def run(soup, url, **kwargs):
    if not soup:
        return 0, None

    text = soup.get_text().lower()

    email = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+", text)
    phone = re.search(r"\+?[0-9][0-9\-\s]{7,}", text)

    if email:
        return 1, email.group(0)

    if phone:
        return 1, phone.group(0)

    return 0, None
