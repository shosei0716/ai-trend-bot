"""formatter モジュールの単体テスト（DUMMY_MODE使用）"""

from unittest.mock import patch

from formatter.claude_formatter import format_post, _DUMMY_OUTPUT


@patch("formatter.claude_formatter.DUMMY_MODE", True)
def test_format_post_dummy_mode():
    article = {"title": "Test AI News", "source": "reddit", "score": 100, "url": "https://example.com"}
    result = format_post(article)

    assert result == _DUMMY_OUTPUT
    assert "【今日のAI変化】" in result
    assert "◾︎何が起きた？" in result
    assert "◾︎なぜ重要？" in result
    assert "◾︎今日やること" in result


@patch("formatter.claude_formatter.DUMMY_MODE", False)
@patch("formatter.claude_formatter.ANTHROPIC_API_KEY", "")
def test_format_post_no_api_key():
    article = {"title": "Test", "source": "reddit", "score": 1, "url": ""}
    try:
        format_post(article)
        assert False, "Should have raised RuntimeError"
    except RuntimeError as e:
        assert "ANTHROPIC_API_KEY" in str(e)
