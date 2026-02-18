from typing import Dict, List

import requests

from config import REDDIT_SUBREDDIT, REDDIT_LIMIT


def fetch_reddit_posts() -> List[Dict]:
    """Reddit r/{subreddit} から上位AI関連投稿を取得する。"""
    url = f"https://www.reddit.com/r/{REDDIT_SUBREDDIT}/hot.json"
    headers = {"User-Agent": "ai-trend-bot/1.0"}
    params = {"limit": REDDIT_LIMIT}

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[Reddit] 取得エラー: {e}")
        return []

    try:
        children = resp.json()["data"]["children"]
    except (KeyError, ValueError) as e:
        print(f"[Reddit] パースエラー: {e}")
        return []

    posts = []
    for child in children:
        d = child["data"]
        posts.append({
            "source": "reddit",
            "title": d.get("title", ""),
            "score": d.get("score", 0),
            "url": d.get("url", ""),
        })

    return posts
