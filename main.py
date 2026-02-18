"""AI Trend Bot - メインエントリポイント

Reddit / HackerNews からAIニュースを収集し、
Claude APIで整形してX投稿用テキストを生成する。
"""

import os
import sys
from typing import List, Dict, Optional

from collector.reddit import fetch_reddit_posts
from collector.hackernews import fetch_hackernews_posts
from formatter.claude_formatter import format_post
from config import OUTPUT_DIR, OUTPUT_FILE


def select_top_article(posts: List[Dict]) -> Optional[Dict]:
    """スコアが最も高い記事を1件返す。"""
    if not posts:
        return None
    return max(posts, key=lambda p: p.get("score", 0))


def save_output(text: str) -> str:
    """整形済みテキストを output/today_post.txt に上書き保存する。"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(text)
    return OUTPUT_FILE


def main() -> None:
    print("=== AI Trend Bot 起動 ===")

    # 1. ニュース収集
    print("[1/4] Reddit からニュース取得中...")
    reddit_posts = fetch_reddit_posts()
    print(f"  → {len(reddit_posts)} 件取得")

    print("[2/4] HackerNews からニュース取得中...")
    hn_posts = fetch_hackernews_posts()
    print(f"  → {len(hn_posts)} 件取得")

    # 2. 統合 & 選択
    all_posts = reddit_posts + hn_posts
    article = select_top_article(all_posts)

    if article is None:
        print("[WARN] ニュースが0件のため、Claude APIを呼ばず終了します。")
        sys.exit(0)

    print(f"[3/4] 選択記事: {article['title']} (score={article['score']})")

    # 3. Claude で整形（1回のみ）
    try:
        post_text = format_post(article)
    except RuntimeError as e:
        print(f"[ERROR] 整形失敗: {e}")
        sys.exit(1)

    # 4. 保存
    path = save_output(post_text)
    print(f"[4/4] 保存完了: {path}")
    print("---")
    print(post_text)
    print("---")
    print("=== 完了 ===")


if __name__ == "__main__":
    main()
