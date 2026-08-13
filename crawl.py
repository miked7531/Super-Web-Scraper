from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag

def normalize_url(url: str) -> str:
    # Break the URL into its components (scheme, netloc, path, etc.)
    parts = urlsplit(url)

    # Get the hostname and the path
    hostname = parts.netloc
    path = parts.path

    # Remove a trailing slash if present
    path = path.rstrip("/")

    # Combine hostname + path into the normalized URL
    return hostname + path

def get_heading_from_html(html: str) -> str:
    # parse the HTML string into a beautifulsoup object
    soup = BeautifulSoup(html, "html.parser")

    # try to find an <h1> first
    h_tag = soup.find("h1")

    # if no <h1> exists, fall back to <h2>
    if h_tag is None:
        h_tag = soup.find("h2")
    
    # safely extract the text if we found a tag, otherwise return empty string
    return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""
    
def get_first_paragraph_from_html(html: str) -> str:
    # parse the html string into a beautifulsoup object
    soup = BeautifulSoup(html, "html.parser")

    # First, try to find a <main> tag
    main = soup.find("main")

    if main is not None:
        # if <main> exists, look for the first <p> inside it
        p_tag = main.find("p")
    else:
        # otherwise, just take the first <p> in the whole document
        p_tag = soup.find("p")
    
    # safely extract the text if a <p> tag is found, otherwise return an empty string
    return p_tag.get_text(strip=True) if isinstance(p_tag, Tag) else ""

def get_urls_from_html(html: str, base_url: str) -> list[str]:
    # parse the HTML
    soup = BeautifulSoup(html, "html.parser")

    # find all <a> tags
    anchors = soup.find_all("a")

    urls = []
    for anchor in anchors:
        # get the href attribute (may be None)
        href = anchor.get("href")
        if href:
            # turn relative URLs into absolute ones
            absolute_url = urljoin(base_url, href)
            urls.append(absolute_url)
    
    return urls

def get_images_from_html(html: str, base_url: str) -> list[str]:
    # Parse the HTML
    soup = BeautifulSoup(html, "html.parser")

    # Find all <img> tags
    images = soup.find_all("img")

    urls = []
    for img in images:
        # Get the src attribute (may be None)
        src = img.get("src")
        if src:
            # Turn relative URLs into absolute ones
            absolute_url = urljoin(base_url, src)
            urls.append(absolute_url)
    return urls

def extract_page_data(html: str, page_url: str) -> dict:
    # Build a structured dictionary of all the useful page information
    return {
        "url": page_url,    # the crawled page
        "heading": get_heading_from_html(html), #h1 or h2
        "first_paragraph": get_first_paragraph_from_html(html),     #best paragraph
        "outgoing_links": get_urls_from_html(html, page_url),   # all <a> hrefs
        "image_urls": get_images_from_html(html, page_url),    # all <img> srcs
    }