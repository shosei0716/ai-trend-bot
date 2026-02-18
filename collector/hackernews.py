from typing import Dict, List

import requests

from config import HACKERNEWS_LIMIT


_BASE_URL = "https://hacker-news.firebaseio.com/v0"
_AI_KEYWORDS = ["ai", "gpt", "llm", "openai", "claude", "gemini", "machine learning",
                "deep learning", "neural", "transformer", "anthropic"]


def _is_ai_related(title: str) -> bool:
    lower = title.lower()
    return any(kw in lower for kw in _AI_KEYWORDS)


def fetch_hackernews_posts() -> List[Dict]:
    """HackerNews トップストーリーからAI関連を抽出する。"""
    try:
        resp = requests.get(f"{_BASE_URL}/topstories.json", timeout=10)
        resp.raise_for_status()
        story_ids = resp.json()[:30]
    except (requests.RequestException, ValueError) as e:
        print(f"[HN] ストーリーID取得エラー: {e}")
        return []

    posts = []
    for sid in story_ids:
        if len(posts) >= HACKERNEWS_LIMIT:
            break
        try:
            item_resp = requests.get(f"{_BASE_URL}/item/{sid}.json", timeout=10)
            item_resp.raise_for_status()
            item = item_resp.json()
        except (requests.RequestException, ValueError):
            continue

        title = item.get("title", "")
        if not _is_ai_related(title):
            continue

        posts.append({
            "source": "hackernews",
            "title": title,
            "score": item.get("score", 0),
            "url": item.get("url", ""),
        })

    return posts
