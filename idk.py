from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from tools import search_rss, fetch_article
import yaml

with open("config.yaml") as f:
    CFG = yaml.safe_load(f)

llm = ChatOllama(model=CFG["llm"]["model"], temperature=CFG["llm"]["temperature"])

class NewsState(TypedDict):
    query: str
    urls: List[str]
    articles: List[dict]
    digest: str

def search_node(state: NewsState):
    urls = search_rss(state["query"])
    return {"urls": urls}

def scrape_node(state: NewsState):
    articles = []
    for url in state["urls"]:
        try:
            articles.append({"url": url, "content": fetch_article(url)})
        except Exception as e:
            print(f"Skip {url}: {e}")
    return {"articles": articles}

def summarize_node(state: NewsState):
    summary_prompt = ChatPromptTemplate.from_template(
        "Summarize this article about '{query}' in 3 bullet points with key facts. Cite URL.\nURL: {url}\nArticle:\n{article}"
    )
    summaries = []
    for a in state["articles"]:
        out = llm.invoke(summary_prompt.format(query=state["query"], url=a["url"], article=a["content"]))
        summaries.append({"url": a["url"], "summary": out.content})

    digest_prompt = ChatPromptTemplate.from_template(
        "Combine these summaries into a ~1300-1600 word 10 minute read digest for '{query}'. Group by theme. Summaries:\n{summaries}"
    )
    combined = "\n\n".join([s["summary"] for s in summaries])
    digest = llm.invoke(digest_prompt.format(query=state["query"], summaries=combined)).content
    return {"digest": digest}

def build_graph():
    g = StateGraph(NewsState)
    g.add_node("search", search_node
    g.add_node("scrape", scrape_node)
    g.add_node("summarize", summarize_node)
    g.set_entry_point("search")
    g.add_edge("search", "scrape")
    g.add_edge("scrape", "summarize")
    g.add_dege("summarize", END)
    return g.compile()
