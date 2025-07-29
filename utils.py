import requests

BASE_URL = 'http://localhost:5000/api/v1/news'


def parse_intent_entity(output: str):
    intent, entity = output.split(":", 1)
    intent = intent.strip()
    entity = entity.strip()
    
    if intent == "nearby":
        lat, lon, radius = entity.split(",")
        entity = [lat.strip(), lon.strip(), radius.strip()]
    
    return intent, entity

class APIError(Exception):
    """Custom exception for API errors"""
    def __init__(self, status_code, message):
        super().__init__(f"HTTP {status_code}: {message}")
        self.status_code = status_code
        self.message = message


def _handle_response(resp):
    """
    Check the response for HTTP errors and return JSON data.
    Raises APIError on non-2xx responses.
    """
    try:
        data = resp.json()
    except ValueError:
        resp.raise_for_status()
        return resp.text

    if not resp.ok:
        error_msg = data.get('error', data)
        raise APIError(resp.status_code, error_msg)
    return data


def get_by_category(category):
    """
    Fetch articles filtered by category.
    Returns list of article IDs.
    """
    resp = requests.get(f"{BASE_URL}/category", params={'category': category})
    print('resp: ', resp)
    return _handle_response(resp)


def get_by_score(min_score):
    """
    Fetch articles with relevance_score >= min_score.
    Returns list of article IDs.
    """
    resp = requests.get(f"{BASE_URL}/score", params={'min_score': min_score})
    return _handle_response(resp)


def search_articles(query):
    """
    Perform full-text search on title and description.
    Returns list of dicts with 'id' and 'score'.
    """
    resp = requests.get(f"{BASE_URL}/search", params={'query': query})
    return _handle_response(resp)


def get_by_source(source):
    """
    Fetch articles by source name.
    Returns list of article IDs.
    """
    resp = requests.get(f"{BASE_URL}/source", params={'source': source})
    return _handle_response(resp)


def get_nearby(lat, lon, radius=10):
    """
    Fetch articles within `radius` km of (lat, lon).
    Returns list of dicts with 'id' and 'distance_km'.
    """
    resp = requests.get(
        f"{BASE_URL}/nearby",
        params={'lat': lat, 'lon': lon, 'radius': radius}
    )
    return _handle_response(resp)