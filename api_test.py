from requests import get, post, put, delete
from pprint import pprint

pprint(
    post("http://localhost:5000/api/groups/ZxnC8PXNx9ZGAsLV",
         json={"name": "apigroup", "invites": ["user@api.ii"]}).json()
)
