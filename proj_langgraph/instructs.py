import json, feedparser, requests
from bs4 import BeautifulSoup

with open("sources.json") as f:
    sources = json.load(f)

FEEDS = SOURCES["feeds"]
ALLOWED = set(SOURCES["allowed_domains"])

def search_rss(query: str):
    """Searches the RSS feeds for the given query in title and description."""
    ursl = []
    for url_feed in FEEDS:
        data = feedparser.parse(url_feed)
        for entry in data.entries[:10]:
            title = entry.title.lower()
            summary = entry.summary.lower() if hasattr(entry, "summary") else ""
            if  query.lower() in title or query.lower() in summary:
                ursl = entry.link
                domain = entry.link.split("/")[2]
                if domain in ALLOWED:
                    ursl.append(entry.link)
    return list(dict.fromkeys(ursl))  # Remove duplicates while preserving order

def fetch_article(url: str) -> str:
    """Fetches the article content from the given URL."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0"}
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "aside"]): tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    return text[:8000]