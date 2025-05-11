import re
import os
import requests
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader

load_dotenv()

# Function to use SerpAPI and retrieve page content
def search_and_retrieve(query):
    serpapi_key = os.getenv('SERPAPI_KEY')
    if not serpapi_key:
        raise Exception("SERPAPI_KEY not set in .env")

    search_url = "https://serpapi.com/search"
    params = {
        'q': query,
        'api_key': serpapi_key,
        'engine': 'google_news',   
        'num': 5
    }

    response = requests.get(search_url, params=params)
    results = response.json().get('news_results', [])
    
    web_content = []
    try:
        for result in results[:5]:
            url = result.get('link')
            snippet = result.get('snippet', '')
            if url:
                try:
                    loader = WebBaseLoader(url)
                    documents = loader.load()
                    content = documents[0].page_content if documents else ""
                except Exception as e:
                    content = snippet
                    print(f"Failed to retrieve {url}: {e}")
                content = re.sub(r'\s+', ' ', content).strip()
                web_content.append({
                    'url': url,
                    'content': content
                })
    except Exception as e:
        print(f"Error parsing search results: {e}")
    
    return web_content

