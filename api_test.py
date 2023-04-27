from requests import get, post, put, delete

print(
    get("http://localhost:5000/api//groups/",
        json={
            "apikey": "5X5N3unrULbnZB79"
        }
    )
)
