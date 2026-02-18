import os


# --- API Keys ---
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# --- Safety Flags ---
DUMMY_MODE = os.environ.get("DUMMY_MODE", "false").lower() == "true"

# --- Claude API Settings ---
CLAUDE_MODEL = "claude-sonnet-4-5-20250929"
CLAUDE_MAX_TOKENS = 800
CLAUDE_TEMPERATURE = 0.5

# --- Collector Settings ---
REDDIT_SUBREDDIT = "artificial"
REDDIT_LIMIT = 5
HACKERNEWS_LIMIT = 5

# --- Output ---
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "today_post.txt")
