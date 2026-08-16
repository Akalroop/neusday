from typing import TypingDict, List
from Langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from tools import search_rss, fetch_article
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

llm = ChatOllama(model=config["llm"]["model"], temperature=config["llm"]["temperature"])

class NewsState(TypedDict):
    query: str
    urls: List[str]
    articles: List[dict]
    digest:str

def search_node(state: NewsState):
    urls = search_rss(state["query"])
    return{"urls": urls}

def scrape_node(state: NewsState):
    articles[]
    for url in state["urls"]:
        try:
            articles.append({"urls":url, "content": fetch_article(url)})
        except Exception as e:
            print(f"Skip {url}: {e}")
    return {"articles": articles}

def summary_node(state: NewsState):
    summary_prompt = ChatPromptTemplate.from_tempelate(
        "Summarize this article about {query} in 3 bullet points with key facts. Cite URL.\nURL:
        {url}\nArticle:\n{article}"
    )
    summaries = []