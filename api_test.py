from requests import get, post, put, delete

print(
    get("http://127.0.0.1:5000/api/groups/",
        params={
            "apikey": "5X5N3unrULbnZB79"
        }
    )
)
