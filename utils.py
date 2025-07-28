import requests

BASE_URL = 'http://localhost:5000'


def get_by_category(category):
    """
    Fetch articles filtered by category.
    Returns list of article IDs.
    """
    resp = requests.get(f"{BASE_URL}/category", params={'category': category})
    resp.raise_for_status()
    return resp.json()


def get_by_score(min_score):
    """
    Fetch articles with relevance_score >= min_score.
    Returns list of article IDs.
    """
    resp = requests.get(f"{BASE_URL}/score", params={'min_score': min_score})
    resp.raise_for_status()
    return resp.json()


def search_articles(query):
    """
    Perform full-text search on title and description.
    Returns list of dicts with 'id' and 'score'.
    """
    resp = requests.get(f"{BASE_URL}/search", params={'query': query})
    resp.raise_for_status()
    return resp.json()


def get_by_source(source):
    """
    Fetch articles by source name.
    Returns list of article IDs.
    """
    resp = requests.get(f"{BASE_URL}/source", params={'source': source})
    resp.raise_for_status()
    return resp.json()


def get_nearby(lat, lon, radius=10):
    """
    Fetch articles within `radius` km of (lat, lon).
    Returns list of dicts with 'id' and 'distance_km'.
    """
    resp = requests.get(
        f"{BASE_URL}/nearby",
        params={'lat': lat, 'lon': lon, 'radius': radius}
    )
    resp.raise_for_status()
    return resp.json()