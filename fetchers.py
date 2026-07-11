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
    url = f"https://api.lever.co/v0/postings/{company}?mode=json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        jobs: List[Job] = []
        for job in data:
            jobs.append(Job(
                id=str(job["id"]),
                title=job["text"],
                company=company.capitalize(),
                location=job.get("categories", {}).get("location", "Unknown"),
                url=job["hostedUrl"],
                source="Lever"
            ))
        return jobs
    except Exception as e:
        print(f"Error fetching Lever jobs for {company}: {e}")
        return []
