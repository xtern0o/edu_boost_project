from requests import get, post, put, delete
from pprint import pprint

pprint(
    post("http://localhost:5000/api/groups/trGdN5kwp1VTe06O", params={}).json()

)
