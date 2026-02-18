import anthropic

from config import (
    ANTHROPIC_API_KEY,
    CLAUDE_MAX_TOKENS,
    CLAUDE_MODEL,
    CLAUDE_TEMPERATURE,
    DUMMY_MODE,
)

_DUMMY_OUTPUT = """【今日のAI変化】

◾︎何が起きた？
→ OpenAIが新モデルを発表し、推論性能が大幅に向上した。

◾︎なぜ重要？
→ コーディングや数学の分野で既存モデルを超え、AI活用の幅が広がる。

◾︎今日やること
→ 新モデルのAPIドキュメントを確認し、既存プロジェクトでの活用可能性を検討しよう。"""

_SYSTEM_PROMPT = (
    "あなたはAIトレンド要約の専門家です。"
    "与えられたニュースタイトルを元に、日本語でX(Twitter)投稿用テキストを生成してください。"
    "300〜350文字以内で、以下のフォーマットに厳密に従ってください。\n\n"
    "【今日のAI変化】\n\n"
    "◾︎何が起きた？\n→ \n\n"
    "◾︎なぜ重要？\n→ \n\n"
    "◾︎今日やること\n→ "
)


def format_post(article: dict) -> str:
    """記事情報を受け取り、X投稿用テキストを返す。

    DUMMY_MODE=true の場合は Claude API を呼ばず固定文を返す。
    """
    if DUMMY_MODE:
        print("[Formatter] DUMMY_MODE: Claude APIをスキップ")
        return _DUMMY_OUTPUT

    if not ANTHROPIC_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY が設定されていません")

    user_message = (
        f"以下のAIニュースについて投稿文を作成してください。\n"
        f"タイトル: {article['title']}\n"
        f"ソース: {article['source']}\n"
        f"URL: {article.get('url', 'N/A')}"
    )

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=CLAUDE_MAX_TOKENS,
            temperature=CLAUDE_TEMPERATURE,
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )
        return response.content[0].text
    except anthropic.APIError as e:
        raise RuntimeError(f"Claude API エラー: {e}") from e
