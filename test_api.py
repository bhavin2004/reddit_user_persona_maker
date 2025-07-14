import json

with open("data_cache/spez_posts_1_comments_1.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    print(data)