import re


def url_to_image(text):
    if not text:
        return ''

    match_image = re.search(r'src=[\'"]([^\'"]+)[\'"]', text)
    if match_image:
        return match_image.group(1)

    match_page = re.search(r'https?://ibb\.co/([A-Za-z0-9]+)', text)
    if match_page:
        pattern_of_image = match_page.group(1)
        return f"https://i.ibb.co/{pattern_of_image}/image.jpg"

    if "i.ibb.co" in text:
        return text

    return text
