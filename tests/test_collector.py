"""collector モジュールの単体テスト（モック使用）"""

from unittest.mock import patch, MagicMock

from collector.reddit import fetch_reddit_posts
from collector.hackernews import fetch_hackernews_posts


# ============================
# Reddit テスト
# ============================

def _mock_reddit_response():
    return {
        "data": {
            "children": [
                {"data": {"title": "New GPT-5 released", "score": 500, "url": "https://example.com/1"}},
                {"data": {"title": "AI regulation update", "score": 300, "url": "https://example.com/2"}},
            ]
        }
    }


@patch("collector.reddit.requests.get")
def test_fetch_reddit_posts_success(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = _mock_reddit_response()
    mock_resp.raise_for_status = MagicMock()
    mock_get.return_value = mock_resp

    posts = fetch_reddit_posts()
    assert len(posts) == 2
    assert posts[0]["source"] == "reddit"
    assert posts[0]["title"] == "New GPT-5 released"
    assert posts[0]["score"] == 500


@patch("collector.reddit.requests.get")
def test_fetch_reddit_posts_network_error(mock_get):
    import requests
    mock_get.side_effect = requests.RequestException("timeout")

    posts = fetch_reddit_posts()
    assert posts == []


# ============================
# HackerNews テスト
# ============================

def _mock_hn_item(sid, title, score):
    mock = MagicMock()
    mock.json.return_value = {"id": sid, "title": title, "score": score, "url": f"https://hn.example.com/{sid}"}
    mock.raise_for_status = MagicMock()
    return mock


@patch("collector.hackernews.requests.get")
def test_fetch_hackernews_posts_success(mock_get):
    top_resp = MagicMock()
    top_resp.json.return_value = [101, 102, 103]
    top_resp.raise_for_status = MagicMock()

    item_ai = _mock_hn_item(101, "New AI transformer model", 200)
    item_non = _mock_hn_item(102, "Rust 2.0 released", 150)
    item_llm = _mock_hn_item(103, "LLM benchmarks updated", 180)

    mock_get.side_effect = [top_resp, item_ai, item_non, item_llm]

    posts = fetch_hackernews_posts()
    assert len(posts) == 2
    assert posts[0]["title"] == "New AI transformer model"
    assert posts[1]["title"] == "LLM benchmarks updated"


@patch("collector.hackernews.requests.get")
def test_fetch_hackernews_posts_network_error(mock_get):
    import requests
    mock_get.side_effect = requests.RequestException("connection error")

    posts = fetch_hackernews_posts()
    assert posts == []
