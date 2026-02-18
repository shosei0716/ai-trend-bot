"""main.py の結合テスト"""

import os
from unittest.mock import patch

from main import select_top_article, save_output, main
from config import OUTPUT_FILE


def test_select_top_article():
    posts = [
        {"title": "A", "score": 10},
        {"title": "B", "score": 50},
        {"title": "C", "score": 30},
    ]
    top = select_top_article(posts)
    assert top["title"] == "B"


def test_select_top_article_empty():
    assert select_top_article([]) is None


def test_save_output(tmp_path):
    test_file = tmp_path / "test_post.txt"
    with patch("main.OUTPUT_FILE", str(test_file)), \
         patch("main.OUTPUT_DIR", str(tmp_path)):
        path = save_output("テスト投稿")
    assert os.path.exists(path)
    with open(path, encoding="utf-8") as f:
        assert f.read() == "テスト投稿"


@patch("main.fetch_hackernews_posts")
@patch("main.fetch_reddit_posts")
@patch("main.format_post")
def test_main_integration(mock_format, mock_reddit, mock_hn, tmp_path):
    mock_reddit.return_value = [
        {"title": "AI News", "score": 100, "source": "reddit", "url": "https://example.com"},
    ]
    mock_hn.return_value = []
    mock_format.return_value = "【今日のAI変化】\nテスト"

    test_file = tmp_path / "today_post.txt"
    with patch("main.OUTPUT_FILE", str(test_file)), \
         patch("main.OUTPUT_DIR", str(tmp_path)):
        main()

    assert test_file.exists()
    assert "【今日のAI変化】" in test_file.read_text(encoding="utf-8")
    mock_format.assert_called_once()


@patch("main.fetch_hackernews_posts")
@patch("main.fetch_reddit_posts")
def test_main_no_articles(mock_reddit, mock_hn):
    mock_reddit.return_value = []
    mock_hn.return_value = []

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0


import pytest
