import requests
import json
import sqlite3

key = "0de4aad7f46641acabf091e6199ac629"
url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={key}"

resp = requests.get(url)
print(resp)
print(resp.text)

status_code = resp.status_code
print(status_code)

headers = resp.headers
print(headers)

print()

json_response = resp.json()
print(json_response)

with open("news_data.json", "w") as json_file:
    json.dump(json_response, json_file, indent=4)

with open("news_data.json", "r") as json_file:
    news_data = json.load(json_file)

    articles = news_data.get("articles")
    for article in articles:
        print("author:", article.get("author"))
        print("title:", article.get("title"))
        print("description:", article.get("description"))
        print()

conn = sqlite3.connect("news.db")
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        author TEXT,
        url TEXT,
        published_at TEXT
    )
''')

for article in articles:
    c.execute('''
           INSERT INTO news (title, description, author, url, published_at)
           VALUES (?, ?, ?, ?, ?)
       ''', (
        article.get("title"),
        article.get("description"),
        article.get("author"),
        article.get("url"),
        article.get("publishedAt")
    ))

conn.commit()

conn.close()
