
# from datetime import datetime
# today_str = datetime.today().strftime("%Y-%m-%d")
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field
# from typing import List, Dict, Optional
# import json
# from datetime import datetime, timedelta

# # Import LangChain components
# from langchain_core.tools import tool
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.agents import create_tool_calling_agent, AgentExecutor

# # For the scraping tool
# import requests
# from bs4 import BeautifulSoup


# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware # Import CORS middleware
# from pydantic import BaseModel, Field
# from typing import List, Dict, Optional
# import json
# from datetime import datetime, timedelta



# # --- Your existing scrape_dawn_articles tool definition ---
# @tool
# def scrape_dawn_articles(start_date=None, end_date=None):
#     """
#     Scrapes Dawn articles between given dates, extracts title and content,
#     and returns them in JSON format. If no date is given, defaults to today.
#     This function fetches the top 3 articles from the editorial section of Dawn
#     newspaper for each day in the specified date range.
#     It extracts the title and content of each article and returns them as a list of dictionaries.

#     Args:
#         start_date (str, optional): Format "YYYY-MM-DD". Defaults to today.
#         end_date (str, optional): Format "YYYY-MM-DD". Defaults to today.
#     """
#     # Default to today if no dates are given
#     if start_date is None:
#         start_date = datetime.today().strftime("%Y-%m-%d")
#     if end_date is None:
#         end_date = datetime.today().strftime("%Y-%m-%d")

#     def extract_article_text(url):
#         try:
#             response = requests.get(url)
#             response.raise_for_status()
#         except requests.RequestException as e:
#             print(f"Failed to fetch the URL: {e}")
#             return {"title": "", "content": "", "url": url}

#         soup = BeautifulSoup(response.text, 'html.parser')
#         title_tag = soup.select_one("h1.story__title, h2.story__title")
#         title = title_tag.get_text(strip=True) if title_tag else "No title found"
#         content = "\n".join(p.get_text(strip=True) for p in soup.select(".story__content p"))
#         return {"title": title, "content": content.strip(), "url": url}

#     def get_top_urls(start_date, end_date):
#         all_urls = []
#         start = datetime.strptime(start_date, "%Y-%m-%d")
#         end = datetime.strptime(end_date, "%Y-%m-%d")
#         current = start

#         while current <= end:
#             date_str = current.strftime("%Y-%m-%d")
#             page_url = f"https://www.dawn.com/newspaper/editorial/{date_str}"
#             try:
#                 response = requests.get(page_url)
#                 response.raise_for_status()
#                 soup = BeautifulSoup(response.text, 'html.parser')
#                 count = 0
#                 for a_tag in soup.select("article.story a.story__link[href]"):
#                     href = a_tag.get("href")
#                     if href.startswith("https://www.dawn.com/news/") and href not in all_urls:
#                         all_urls.append(href)
#                         count += 1
#                     if count == 3:
#                         break
#             except requests.RequestException as e:
#                 print(f"[{date_str}] Failed to fetch: {e}")
#             current += timedelta(days=1)
#         return all_urls

#     # Fetch article URLs
#     urls = get_top_urls(start_date, end_date)

#     # Extract article data
#     articles = [extract_article_text(url) for url in urls]

#     return articles


# llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash")
# tools = [scrape_dawn_articles]

# prompt = ChatPromptTemplate.from_messages([
#     ("system", """You are a helpful assistant specialized in scraping and analyzing news articles from the Dawn newspaper editorial section.
# Your primary function is to process user requests related to news articles and their content.

# **IMPORTANT DATE FORMATTING:**
# When using the 'scrape_dawn_articles' tool, always ensure that 'start_date' and 'end_date' arguments are provided in the **"YYYY-MM-DD" format**.
# If the user provides relative dates (e.g., "yesterday", "today", "last week", "June 5th"), you MUST first convert these into their exact "YYYY-MM-DD" calendar dates before calling the tool.
# Today's date is {today_str}.  Use this knowledge for relative date calculations.

# **Conditional Behavior for Article Processing:**
# - **Default Action (when only dates are provided):** If the user's request consists *only* of a date or a date range (e.g., "articles for June 10", "news from 2025-06-05 to 2025-06-07") **AND contains NO other specific output instructions** (e.g., "summarize", "provide urls", "list headlines", "find key points", "show vocabulary", etc.), you MUST scrape the articles and return a list of all article **titles along with their URLs** for that time period. Do NOT include summaries, vocabulary, idioms, or anything else unless explicitly asked.

# - **Specific Request Priority:** If the user provides *any* specific instruction or requests a particular type of information about the articles (e.g., "I just want the URLs", "summarize the articles", "find key points", "list headlines", "show topics", "give vocabulary words", "show idioms"), you MUST prioritize and fulfill *only* that specific request. Do NOT provide any other information (e.g., vocabulary, phrases, summaries, or links) unless it is explicitly requested.

# - **Topic-Specific Requests:** If the user asks for article information (e.g., titles, URLs, summaries) related to a **specific topic** (e.g., "economy", "climate", "politics", "society issues") within a **specific date or date range**, you MUST:
#     1. Scrape all articles for the given time period.
#     2. Filter them based on relevance to the requested topic.
#     3. Return only those articles that match the topic.
#     - If the user requests **URLs**, only return the links of the topic-relevant articles.
#     - If the user requests **summaries**, summarize only the relevant articles.
#     - If no specific instruction is provided, return **article titles with their URLs** related to the topic.
#     - If no date or range is specified, default to the **last three (3) days**, and explicitly state that this is the range being used.

# **Topic Restriction:**
# - You can only answer questions or fulfill requests that are directly related to news articles from the Dawn newspaper.
# - If the user requests information, summaries, or URLs about a **general topic or issue** (e.g., economy, society issues, education, climate change, etc.), interpret this as a valid request to search Dawn articles for that topic. You MUST then scrape and filter Dawn articles to find the ones relevant to the requested topic.
# - For any clearly unrelated query (e.g., math problems, coding help, or non-news topics), you MUST respond by stating that you can only assist with news-related queries from the Dawn newspaper.
# """),
#     ("human", "{input}"),
#     ("ai", "Use the tools to answer the question."),
#     ("placeholder", "{agent_scratchpad}")
# ])



# agent = create_tool_calling_agent(llm, tools, prompt)
# agent_exec = AgentExecutor(agent=agent, tools=tools, verbose=True)


# # --- FastAPI Application Setup ---
# app = FastAPI(
#     title="Dawn News Scraper Agent",
#     description="An AI agent that scrapes and analyzes articles from Dawn newspaper editorial section.",
#     version="1.0.0",
# )

# # Add CORS middleware
# origins = [
#     "http://localhost:3000",  
#     "https://dawn-ai-frontend.vercel.app/", 
#     "https://dawn-ai-frontend.vercel.app", 
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"], # Allow all HTTP methods (GET, POST, etc.)
#     allow_headers=["*"], # Allow all headers (like Content-Type)
# )

# class AgentQuery(BaseModel):
#     query: str = Field(..., description="The natural language query for the agent.")

# class AgentResponse(BaseModel):
#     response: str
#     articles: Optional[List[Dict]] = Field(None, description="List of scraped articles if applicable.")

# @app.get("/")
# async def root():
#     return {"message": "Welcome to the Dawn News Scraper Agent API. Use the /invoke endpoint to interact with the agent."}

# @app.post("/invoke", response_model=AgentResponse)
# async def invoke_agent(query_body: AgentQuery):
#     """
#     Invokes the LangChain agent with the provided natural language query.
#     """
#     try:
#         # The agent.invoke method returns a dictionary
#         # agent_result = agent_exec.invoke({"input": query_body.query})
#         agent_result = agent_exec.invoke({
#             "input": query_body.query,
#             "today_str": today_str
#         })
#         # The output of the agent is typically in agent_result['output']
#         # The tool output might also be part of the scratchpad, or directly available
#         # if the agent's final answer is just the tool output.

#         # If the agent directly returns the articles (e.g., if the user asked for URLs),
#         # we can try to parse them. Otherwise, we'll just return the agent's text output.
#         # This part might need refinement based on how your agent's final output looks.

#         # A common pattern is for the agent's 'output' to be the text response.
#         # If the tool directly provides a list of articles, you might need to
#         # inspect agent_result to see if that data is present.
        
#         # For simplicity, let's assume the agent's primary text output is in 'output'
#         # and we can potentially extract article data if the query was for scraping directly.
        
#         # Check if the last tool call was 'scrape_dawn_articles' and if its output
#         # is part of the final response, or if the agent explicitly returned it.
        
#         articles_data = None
#         # A more robust way would be to inspect agent_result['intermediate_steps']
#         # if you want to extract tool outputs specifically.
#         # For now, we'll try to infer if the primary output is text or structured articles.

#         # If the agent is instructed to just scrape and provide articles,
#         # its 'output' might be a string representation of the articles, or
#         # it might include them in the `agent_result` directly if configured.
        
#         # Let's try to parse the output if it looks like JSON from the tool.
#         # This is a bit of a heuristic. A better way would be to define a specific
#         # output structure from your agent.
        
#         output_content = agent_result.get('output', '')
#         try:
#             parsed_output = json.loads(output_content)
#             if isinstance(parsed_output, list) and all(isinstance(item, dict) and "title" in item for item in parsed_output):
#                 articles_data = parsed_output
#         except json.JSONDecodeError:
#             pass # Not JSON, treat as regular text response
        
#         # If articles_data is still None, it means the agent's primary output
#         # was text, not structured articles.
#         final_response_text = output_content if not articles_data else "Articles scraped successfully."


#         return AgentResponse(response=final_response_text, articles=articles_data)

#     except Exception as e:
#         # Log the full exception for debugging in production
#         print(f"Error invoking agent: {e}")
#         raise HTTPException(status_code=500, detail=f"Internal server error: {e}")



from datetime import datetime
today_str = datetime.today().strftime("%Y-%m-%d")
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import json
from datetime import datetime, timedelta
import os
from typing import List, Dict
import re

# Import LangChain components
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor

# For the scraping tool
import requests
from bs4 import BeautifulSoup


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # Import CORS middleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import json
from datetime import datetime, timedelta



# --- Your existing scrape_dawn_articles tool definition ---
@tool
def scrape_dawn_articles(start_date=None, end_date=None):
    """
    Scrapes Dawn articles between given dates, extracts title and content,
    and returns them in JSON format. If no date is given, defaults to today.
    This function fetches the top 3 articles from the editorial section of Dawn
    newspaper for each day in the specified date range.
    It extracts the title and content of each article and returns them as a list of dictionaries.

    Args:
        start_date (str, optional): Format "YYYY-MM-DD". Defaults to today.
        end_date (str, optional): Format "YYYY-MM-DD". Defaults to today.
    """
    # Default to today if no dates are given
    if start_date is None:
        start_date = datetime.today().strftime("%Y-%m-%d")
    if end_date is None:
        end_date = datetime.today().strftime("%Y-%m-%d")

    def extract_article_text(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to fetch the URL: {e}")
            return {"title": "", "content": "", "url": url}

        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.select_one("h1.story__title, h2.story__title")
        title = title_tag.get_text(strip=True) if title_tag else "No title found"
        content = "\n".join(p.get_text(strip=True) for p in soup.select(".story__content p"))
        return {"title": title, "content": content.strip(), "url": url}

    def get_top_urls(start_date, end_date):
        all_urls = []
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        current = start

        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            page_url = f"https://www.dawn.com/newspaper/editorial/{date_str}"
            try:
                response = requests.get(page_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                count = 0
                for a_tag in soup.select("article.story a.story__link[href]"):
                    href = a_tag.get("href")
                    if href.startswith("https://www.dawn.com/news/") and href not in all_urls:
                        all_urls.append(href)
                        count += 1
                    if count == 3:
                        break
            except requests.RequestException as e:
                print(f"[{date_str}] Failed to fetch: {e}")
            current += timedelta(days=1)
        return all_urls

    # Fetch article URLs
    urls = get_top_urls(start_date, end_date)

    # Extract article data
    articles = [extract_article_text(url) for url in urls]

    return articles

from langchain.agents import tool
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

@tool
def scrape_dawn_opinion_articles(start_date=None, end_date=None):
    """
    Scrapes Dawn opinion articles between given dates, extracts title and content,
    and returns them in JSON format. If no date is given, defaults to today.
    This function fetches the top 3 articles from the opinion/column section of Dawn
    newspaper for each day in the specified date range.
    It extracts the title and content of each article and returns them as a list of dictionaries.

    Args:
        start_date (str, optional): Format "YYYY-MM-DD". Defaults to today.
        end_date (str, optional): Format "YYYY-MM-DD". Defaults to today.
    """
    # Default to today if no dates are given
    if start_date is None:
        start_date = datetime.today().strftime("%Y-%m-%d")
    if end_date is None:
        end_date = datetime.today().strftime("%Y-%m-%d")

    def extract_article_text(url, date):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to fetch the URL: {e}")
            return {"title": "", "content": "", "url": url, "date": date}

        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.select_one("h1.story__title, h2.story__title")
        title = title_tag.get_text(strip=True) if title_tag else "No title found"
        content = "\n".join(p.get_text(strip=True) for p in soup.select(".story__content p"))
        return {"title": title, "content": content.strip(), "url": url, "date": date}

 
        

    def get_top_urls(start_date, end_date):
        all_urls = []
        date_url_map = []
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        current = start

        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            page_url = f"https://www.dawn.com/newspaper/column/{date_str}"
            try:
                response = requests.get(page_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                count = 0
                for a_tag in soup.select("article.story a.story__link[href]"):
                    href = a_tag.get("href")
                    if href.startswith("https://www.dawn.com/news/") and href not in all_urls:
                        all_urls.append(href)
                        date_url_map.append((href, date_str))
                        count += 1
                    if count == 4:
                        break
            except requests.RequestException as e:
                print(f"[{date_str}] Failed to fetch: {e}")
            current += timedelta(days=1)
        return date_url_map

    # Fetch article URLs with dates
    urls_with_dates = get_top_urls(start_date, end_date)

    # Extract article data with date
    articles = [extract_article_text(url, date) for url, date in urls_with_dates]

    return articles


from typing import List, Dict

@tool
def save_articles_json(articles: List[Dict], filename: str = "articles.json") -> str:
    """
    Saves a list of article dictionaries to a JSON file in the specified format.
    Each article should have at least 'date', 'title', 'content' or 'summary', and 'url'.
    Adds an empty 'keywords' list and a 'source' key (determined from the URL) to each article.
    Returns the path to the saved file.
    """
    def infer_source(url: str) -> str:
        if "dawn.com" in url:
            return "dawn"
        elif "tribune.com.pk" in url:
            return "tribune"
        elif "paradigmshift.com.pk" in url:
            return "paradigmshift"
        else:
            return "unknown"

    formatted = []
    for article in articles:
        content_or_summary = article.get("content") or article.get("summary") or ""
        url = article.get("url", "")
        source = article.get("source") or infer_source(url)
        formatted.append({
            "date": article.get("date", ""),
            "title": article.get("title", ""),
            "content": content_or_summary,
            "url": url,
            "source": source,
            "keywords": []
        })
    os.makedirs("saved_articles", exist_ok=True)
    file_path = os.path.join("saved_articles", filename)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(formatted, f, ensure_ascii=False, indent=2)
    return f"Articles saved to {file_path}"


@tool
def scrape_tribune_editorials():
    """
    Scrapes the top 6 editorial articles from the first page of The Express Tribune.
    Returns a list of dicts, each with 'title', 'date', 'content', and 'url'.
    """
    base_url = "https://tribune.com.pk/editorial"
    articles = []

    # Get top 6 editorial URLs from the first page
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.select('li div.horiz-news3-caption a[href^="https://tribune.com.pk/story/"]')
        urls = [link.get('href') for link in links if link.get('href')][:6]
    except Exception as e:
        print(f"Error fetching editorial URLs: {e}")
        return []

    # Scrape each article
    for url in urls:
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, 'html.parser')
            title_tag = soup.select_one('div.story-box-section h1')
            title = title_tag.get_text(strip=True) if title_tag else None
            date_tag = soup.select_one('div.left-authorbox span')
            publish_date = date_tag.get_text(strip=True) if date_tag else None
            content_div = soup.select_one('span.story-text')
            content = []
            if content_div:
                paragraphs = content_div.find_all('p', recursive=False)
                for p_tag in paragraphs:
                    for script_or_style in p_tag(['script', 'style', 'div']):
                        script_or_style.decompose()
                    paragraph_text = p_tag.get_text(strip=True)
                    if paragraph_text:
                        content.append(paragraph_text)
                content = "\n\n".join(content)
            else:
                content = ""
            articles.append({
                "title": title,
                "date": publish_date,
                "content": content,
                "url": url
            })
        except Exception as e:
            print(f"Error scraping article {url}: {e}")
    return articles


@tool
def scrape_paradigmshift_articles() -> list:
    """
    Scrapes the top 3 articles from both the 'International Relations' and 'Pakistan' sections of Paradigm Shift.
    Returns a list of dicts, each with 'section', 'title', 'date', 'url', and 'summary'.
    """
    sections = {
        "International Relations": "https://www.paradigmshift.com.pk/articles/international-relations-articles/",
        "Pakistan": "https://www.paradigmshift.com.pk/articles/pakistan-articles/"
    }
    all_articles = []

    for section_name, url in sections.items():
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            article_cards = soup.select('article.ast-article-post')[:3]
            for card in article_cards:
                # Title and URL
                title_link_tag = card.select_one('h2.entry-title a')
                title = title_link_tag.get_text(strip=True) if title_link_tag else None
                article_url = title_link_tag.get('href') if title_link_tag else None

                # Date
                date_tag = card.select_one('div.entry-meta span.published')
                publish_date = date_tag.get_text(strip=True) if date_tag else None
                if publish_date:
                    publish_date = re.sub(r'\s+', ' ', publish_date).strip()

                # Summary
                summary_div = card.select_one('div.ast-excerpt-container')
                summary = None
                if summary_div:
                    summary_paragraphs = summary_div.find_all('p', recursive=False)
                    summary = "\n\n".join([p.get_text(strip=True) for p in summary_paragraphs if p.get_text(strip=True)])
                    if not summary:
                        summary = summary_div.get_text(strip=True)

                if title and article_url:
                    all_articles.append({
                        "section": section_name,
                        "title": title,
                        "date": publish_date,
                        "url": article_url,
                        "summary": summary
                    })
        except Exception as e:
            print(f"Error scraping section {section_name}: {e}")

    return all_articles


llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash")
# tools = [scrape_dawn_articles]
# tools = [scrape_dawn_articles, scrape_dawn_opinion_articles]
tools = [scrape_dawn_articles, scrape_dawn_opinion_articles, scrape_tribune_editorials,scrape_paradigmshift_articles , scrape_paradigmshift_articles, save_articles_json]

# prompt = ChatPromptTemplate.from_messages([
#     ("system", """You are a helpful assistant specialized in scraping and analyzing news articles from the Dawn newspaper editorial  and Opinion section.
# Your primary function is to process user requests related to news articles and their content.

# **IMPORTANT DATE FORMATTING:**
# When using the 'scrape_dawn_articles' tool, always ensure that 'start_date' and 'end_date' arguments are provided in the **"YYYY-MM-DD" format**.
# If the user provides relative dates (e.g., "yesterday", "today", "last week", "June 5th"), you MUST first convert these into their exact "YYYY-MM-DD" calendar dates before calling the tool.
# Today's date is {today_str}.  Use this knowledge for relative date calculations.

# **Conditional Behavior for Article Processing:**
# - **Default Action (when only dates are provided):** If the user's request consists *only* of a date or a date range (e.g., "articles for June 10", "news from 2025-06-05 to 2025-06-07") **AND contains NO other specific output instructions** (e.g., "summarize", "provide urls", "list headlines", "find key points", "show vocabulary", etc.), you MUST scrape the articles and return a list of all article **titles along with their URLs** for that time period. Do NOT include summaries, vocabulary, idioms, or anything else unless explicitly asked.

# - **Specific Request Priority:** If the user provides *any* specific instruction or requests a particular type of information about the articles (e.g., "I just want the URLs", "summarize the articles", "find key points", "list headlines", "show topics", "give vocabulary words", "show idioms"), you MUST prioritize and fulfill *only* that specific request. Do NOT provide any other information (e.g., vocabulary, phrases, summaries, or links) unless it is explicitly requested.

# - **Topic-Specific Requests:** If the user asks for article information (e.g., titles, URLs, summaries) related to a **specific topic** (e.g., "economy", "climate", "politics", "society issues") within a **specific date or date range**, you MUST:
#     1. Scrape all articles for the given time period.
#     2. Filter them based on relevance to the requested topic.
#     3. Return only those articles that match the topic.
#     - If the user requests **URLs**, only return the links of the topic-relevant articles.
#     - If the user requests **summaries**, summarize only the relevant articles.
#     - If no specific instruction is provided, return **article titles with their URLs** related to the topic.
#     - If no date or range is specified, default to the **last three (3) days**, and explicitly state that this is the range being used.

# **Topic Restriction:**
# - You can only answer questions or fulfill requests that are directly related to news articles from the Dawn newspaper.
# - If the user requests information, summaries, or URLs about a **general topic or issue** (e.g., economy, society issues, education, climate change, etc.), interpret this as a valid request to search Dawn articles for that topic. You MUST then scrape and filter Dawn articles to find the ones relevant to the requested topic.
# - For any clearly unrelated query (e.g., math problems, coding help, or non-news topics), you MUST respond by stating that you can only assist with news-related queries from the Dawn newspaper.
# """),
#     ("human", "{input}"),
#     ("ai", "Use the tools to answer the question."),
#     ("placeholder", "{agent_scratchpad}")
# ])


prompt = ChatPromptTemplate.from_messages([
    ("system", f"""You are a helpful assistant specialized in scraping and analyzing news articles from the Dawn newspaper's Editorial and Opinion (Column) sections.
Your primary function is to process user requests related to news articles and their content.

**TOOLS AVAILABLE:**
- 'scrape_dawn_articles': Use this tool to scrape articles from the Editorial section.
- 'scrape_dawn_opinion_articles': Use this tool to scrape articles from the Opinion/Column section.
- 'scrape_tribune_editorials': Use for The Tribune News Editorials/Articles
- 'scrape_paradigmshift_articles':Use for ParadigmShift Articles
- 'save_articles_json': If the user requests to save articles as a JSON file, use this tool after scraping.

**WHEN TO USE EACH TOOL:**
- Use 'scrape_dawn_articles' for requests about the Dawn Editorial section.
- Use 'scrape_dawn_opinion_articles' for requests about the Dawn Opinion or Column section.
- Use 'scrape_tribune_editorials' for requests about the Tribune Editorial section.
- Use 'scrape_paradigmshift_articles' for requests about the ParadigmShift Editorial section.
- Use 'save_articles_json' to save json after getting the articles\
- If the user does not specify a section, give articles from both section and also tell which article is from which section

**IMPORTANT DATE FORMATTING:**
When using either tool, always ensure that 'start_date' and 'end_date' arguments are provided in the **"YYYY-MM-DD" format**.
If the user provides relative dates (e.g., "yesterday", "today", "last week", "June 5th"), you MUST first convert these into their exact "YYYY-MM-DD" calendar dates before calling the tool.
Today's date is {today_str}. Use this knowledge for relative date calculations.

When listing articles, you MUST include every article you receive from the tool. Do NOT omit, summarize, or skip any articles. Always present the full list exactly as provided by the tool, unless the user specifically asks for a subset or summary.

**Conditional Behavior for Article Processing:**
- **Default Action (when only dates are provided):** If the user's request consists *only* of a date or a date range (e.g., "articles for June 10", "news from 2025-06-05 to 2025-06-07") **AND contains NO other specific output instructions** (e.g., "summarize", "provide urls", "list headlines", "find key points", "show vocabulary", etc.), you MUST scrape the articles and return a list of all article **titles along with their URLs** for that time period. Do NOT include summaries, vocabulary, idioms, or anything else unless explicitly asked.

- **Specific Request Priority:** If the user provides *any* specific instruction or requests a particular type of information about the articles (e.g., "I just want the URLs", "summarize the articles", "find key points", "list headlines", "show topics", "give vocabulary words", "show idioms"), you MUST prioritize and fulfill *only* that specific request. Do NOT provide any other information (e.g., vocabulary, phrases, summaries, or links) unless it is explicitly requested.

- **Topic-Specific Requests:** If the user asks for article information (e.g., titles, URLs, summaries) related to a **specific topic** (e.g., "economy", "climate", "politics", "society issues") within a **specific date or date range**, you MUST:
    1. Scrape all articles for the given time period using the appropriate tool.
    2. Filter them based on relevance to the requested topic.
    3. Return only those articles that match the topic.
    - If the user requests **URLs**, only return the links of the topic-relevant articles.
    - If the user requests **summaries**, summarize only the relevant articles.
    - If no specific instruction is provided, return **article titles with their URLs** related to the topic.
    - If no date or range is specified, default to the **last three (3) days**, and explicitly state that this is the range being used.

**Section Restriction:**
- You can only answer questions or fulfill requests that are directly related to news articles from the Dawn newspaper's Editorial and Opinion/Column sections.
- If the user requests information, summaries, or URLs about a **general topic or issue** (e.g., economy, society issues, education, climate change, etc.), interpret this as a valid request to search Dawn articles for that topic. You MUST then scrape and filter Dawn articles to find the ones relevant to the requested topic, using the appropriate tool for the section.
- For any clearly unrelated query (e.g., math problems, coding help, or non-news topics), you MUST respond by stating that you can only assist with news-related queries from the Dawn newspaper.
"""),
    ("human", "{input}"),
    ("ai", "Use the tools to answer the question."),
    ("placeholder", "{agent_scratchpad}")
])


agent = create_tool_calling_agent(llm, tools, prompt)
agent_exec = AgentExecutor(agent=agent, tools=tools, verbose=True)


# --- FastAPI Application Setup ---
app = FastAPI(
    title="Dawn News Scraper Agent",
    description="An AI agent that scrapes and analyzes articles from Dawn newspaper editorial section.",
    version="1.0.0",
)

# Add CORS middleware
origins = [
    "http://localhost:3000",  
    "https://dawn-ai-frontend.vercel.app/", 
    "https://dawn-ai-frontend.vercel.app", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"], # Allow all headers (like Content-Type)
)

class AgentQuery(BaseModel):
    query: str = Field(..., description="The natural language query for the agent.")

class AgentResponse(BaseModel):
    response: str
    articles: Optional[List[Dict]] = Field(None, description="List of scraped articles if applicable.")

@app.get("/")
async def root():
    return {"message": "Welcome to the Dawn News Scraper Agent API. Use the /invoke endpoint to interact with the agent."}

@app.post("/invoke", response_model=AgentResponse)
async def invoke_agent(query_body: AgentQuery):
    """
    Invokes the LangChain agent with the provided natural language query.
    """
    try:
        # The agent.invoke method returns a dictionary
        # agent_result = agent_exec.invoke({"input": query_body.query})
        agent_result = agent_exec.invoke({
            "input": query_body.query,
            "today_str": today_str
        })
        # The output of the agent is typically in agent_result['output']
        # The tool output might also be part of the scratchpad, or directly available
        # if the agent's final answer is just the tool output.

        # If the agent directly returns the articles (e.g., if the user asked for URLs),
        # we can try to parse them. Otherwise, we'll just return the agent's text output.
        # This part might need refinement based on how your agent's final output looks.

        # A common pattern is for the agent's 'output' to be the text response.
        # If the tool directly provides a list of articles, you might need to
        # inspect agent_result to see if that data is present.
        
        # For simplicity, let's assume the agent's primary text output is in 'output'
        # and we can potentially extract article data if the query was for scraping directly.
        
        # Check if the last tool call was 'scrape_dawn_articles' and if its output
        # is part of the final response, or if the agent explicitly returned it.
        
        articles_data = None
        # A more robust way would be to inspect agent_result['intermediate_steps']
        # if you want to extract tool outputs specifically.
        # For now, we'll try to infer if the primary output is text or structured articles.

        # If the agent is instructed to just scrape and provide articles,
        # its 'output' might be a string representation of the articles, or
        # it might include them in the `agent_result` directly if configured.
        
        # Let's try to parse the output if it looks like JSON from the tool.
        # This is a bit of a heuristic. A better way would be to define a specific
        # output structure from your agent.
        
        output_content = agent_result.get('output', '')
        try:
            parsed_output = json.loads(output_content)
            if isinstance(parsed_output, list) and all(isinstance(item, dict) and "title" in item for item in parsed_output):
                articles_data = parsed_output
        except json.JSONDecodeError:
            pass # Not JSON, treat as regular text response
        
        # If articles_data is still None, it means the agent's primary output
        # was text, not structured articles.
        final_response_text = output_content if not articles_data else "Articles scraped successfully."


        return AgentResponse(response=final_response_text, articles=articles_data)

    except Exception as e:
        # Log the full exception for debugging in production
        print(f"Error invoking agent: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
