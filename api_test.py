from requests import get, post, put, delete
from pprint import pprint

pprint(
    get("http://localhost:5000/api/groups/ZxnC8PXNx9ZGAsLV").json()
)
