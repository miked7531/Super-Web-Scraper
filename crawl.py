from urllib.parse import urlsplit

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