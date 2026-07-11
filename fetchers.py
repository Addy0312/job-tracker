import requests
import urllib.parse
import feedparser
from bs4 import BeautifulSoup
import html
from typing import List
from models import Job
from config import SERPAPI_KEY, SERPAPI_QUERY, SERPAPI_PAGES, RSS_FEEDS

def fetch_greenhouse_jobs(company: str) -> List[Job]:
    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        jobs: List[Job] = []
        for job in data.get("jobs", []):
            jobs.append(Job(
                id=str(job["id"]),
                title=job["title"],
                company=company.capitalize(),
                location=job.get("location", {}).get("name", "Unknown"),
                url=job["absolute_url"],
                source="Greenhouse"
            ))
        return jobs
    except Exception as e:
        print(f"Error fetching Greenhouse jobs for {company}: {e}")
        return []

def fetch_lever_jobs(company: str) -> List[Job]:
    # Lever has two instances: Global and EU. 
    instances = ["api.lever.co", "api.eu.lever.co"]
    
    for instance in instances:
        url = f"https://{instance}/v0/postings/{company}?mode=json"
        try:
            response = requests.get(url, timeout=10)
            
            # If 404, it might be on the other instance. Try next.
            if response.status_code == 404:
                continue
                
            response.raise_for_status()
            data = response.json()
            
            jobs: List[Job] = []
            for job in data:
                # 1. Extract primary location and allLocations
                categories = job.get("categories", {})
                primary_loc = categories.get("location", "")
                all_locs = categories.get("allLocations", [])
                
                # Combine into a unique set, ignoring empty strings
                locations = set()
                if primary_loc: locations.add(primary_loc)
                for loc in all_locs:
                    if loc: locations.add(loc)
                    
                location_str = ", ".join(locations)
                
                # 2. Extract workplaceType (remote, hybrid, on-site)
                workplace = job.get("workplaceType", "")
                if workplace and workplace.lower() != "unspecified":
                    location_str += f" ({workplace})"
                    
                if not location_str.strip():
                    location_str = "Unknown"
                    
                jobs.append(Job(
                    id=str(job["id"]),
                    title=job["text"],
                    company=company.capitalize(),
                    location=location_str,
                    url=job.get("hostedUrl", ""),
                    source="Lever"
                ))
                
            # If we successfully fetched jobs, return them (don't try the EU instance)
            return jobs
            
        except Exception as e:
            print(f"Error fetching Lever jobs for {company} on {instance}: {e}")
            continue
            
    # If both instances fail or error out
    return []

def fetch_hn_jobs() -> List[Job]:
    try:
        # Strictly search for the official "Who is hiring?" thread by the official author
        query = urllib.parse.quote("Ask HN: Who is hiring?")
        url = f'https://hn.algolia.com/api/v1/search_by_date?query={query}&tags=story,author_whoishiring'
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("hits"):
            return []
            
        # Get the most recent official thread
        latest_thread_id = data['hits'][0]['objectID']
        
        thread_url = f'https://hn.algolia.com/api/v1/items/{latest_thread_id}'
        thread_resp = requests.get(thread_url, timeout=10)
        thread_resp.raise_for_status()
        thread_data = thread_resp.json()
        
        jobs: List[Job] = []
        for comment in thread_data.get('children', []):
            text = comment.get('text')
            if not text:
                continue
                
            clean_text = BeautifulSoup(html.unescape(text), "html.parser").get_text()
            lines = clean_text.strip().split('\n')
            if not lines:
                continue
                
            first_line = lines[0].strip()
            
            # Usually formatted as: "Company | Title | Location | ONSITE/REMOTE"
            parts = first_line.split('|')
            company = parts[0].strip() if len(parts) > 0 else "Hacker News"
            
            # The title is the first line. If it's too long, truncate it nicely.
            job_title = first_line if len(first_line) < 150 else first_line[:147] + "..."
            
            jobs.append(Job(
                id=f"hn_{comment['id']}",
                title=job_title,
                company=company,
                location="See Job Description", # HN locations are too free-text to parse reliably
                url=f"https://news.ycombinator.com/item?id={comment['id']}",
                source="Hacker News"
            ))
            
        return jobs
    except Exception as e:
        print(f"Error fetching Hacker News jobs: {e}")
        return []

def fetch_wwr_jobs() -> List[Job]:
    jobs: List[Job] = []
    try:
        for feed_url in RSS_FEEDS:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                title_parts = entry.title.split(": ", 1)
                if len(title_parts) == 2:
                    company = title_parts[0].strip()
                    title = title_parts[1].strip()
                else:
                    company = "Unknown"
                    title = entry.title
                    
                job_id = getattr(entry, 'id', entry.link)
                    
                jobs.append(Job(
                    id=str(job_id),
                    title=title,
                    company=company,
                    location="Remote",
                    url=entry.link,
                    source="We Work Remotely"
                ))
        return jobs
    except Exception as e:
        print(f"Error fetching RSS jobs: {e}")
        return []

def fetch_google_jobs() -> List[Job]:
    if not SERPAPI_KEY:
        print("Warning: SERPAPI_KEY is not set. Skipping Google Jobs.")
        return []
        
    url = "https://serpapi.com/search.json"
    jobs: List[Job] = []
    
    try:
        for page in range(SERPAPI_PAGES):
            params = {
                "engine": "google_jobs",
                "q": SERPAPI_QUERY,
                "hl": "en",
                "chips": "date_posted:3days",
                "start": page * 10,
                "api_key": SERPAPI_KEY
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = data.get("jobs_results", [])
            if not results:
                break # No more pages available
                
            for job in results:
                job_id = job.get("job_id", "")
                title = job.get("title", "")
                company = job.get("company_name", "")
                location = job.get("location", "Unknown")
                
                apply_links = job.get("apply_options", [])
                job_url = apply_links[0].get("link") if apply_links else job.get("share_link", "")
                
                if not job_id or not title:
                    continue
                    
                jobs.append(Job(
                    id=job_id,
                    title=title,
                    company=company,
                    location=location,
                    url=job_url,
                    source="Google Jobs"
                ))
                
        return jobs
    except Exception as e:
        print(f"Error fetching Google Jobs: {e}")
        return jobs
