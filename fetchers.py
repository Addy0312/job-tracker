import requests
import feedparser
from bs4 import BeautifulSoup
import html
from typing import List
from models import Job

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
        url = 'https://hn.algolia.com/api/v1/search_by_date?query="Ask HN: Who is hiring?"&tags=story'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("hits"):
            return []
            
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
            lines = clean_text.split('\n')
            first_line = lines[0].strip()
            
            parts = first_line.split('|')
            company = parts[0].strip() if len(parts) > 0 else "Hacker News"
            
            jobs.append(Job(
                id=f"hn_{comment['id']}",
                title=first_line[:150],
                company=company,
                location="See Job Description",
                url=f"https://news.ycombinator.com/item?id={comment['id']}",
                source="Hacker News"
            ))
            
        return jobs
    except Exception as e:
        print(f"Error fetching Hacker News jobs: {e}")
        return []

def fetch_wwr_jobs() -> List[Job]:
    try:
        feed = feedparser.parse("https://weworkremotely.com/categories/remote-back-end-programming-jobs.rss")
        jobs: List[Job] = []
        
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
        print(f"Error fetching We Work Remotely jobs: {e}")
        return []
