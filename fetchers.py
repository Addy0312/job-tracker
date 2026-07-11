import requests
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
