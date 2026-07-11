from config import GREENHOUSE_COMPANIES, LEVER_COMPANIES
from fetchers import fetch_greenhouse_jobs, fetch_lever_jobs, fetch_hn_jobs, fetch_wwr_jobs
from filters import is_target_job
from integrations import add_to_notion, send_discord_alert
from db import JobDatabase

def main():
    print("Starting Job Sourcing Pipeline...")
    db = JobDatabase()
    all_jobs = []
    
    for company in GREENHOUSE_COMPANIES:
        jobs = fetch_greenhouse_jobs(company)
        all_jobs.extend(jobs)
        print(f"Fetched {len(jobs)} jobs from Greenhouse: {company}")
        
    for company in LEVER_COMPANIES:
        jobs = fetch_lever_jobs(company)
        all_jobs.extend(jobs)
        print(f"Fetched {len(jobs)} jobs from Lever: {company}")
        
    hn_jobs = fetch_hn_jobs()
    all_jobs.extend(hn_jobs)
    print(f"Fetched {len(hn_jobs)} jobs from Hacker News")
    
    wwr_jobs = fetch_wwr_jobs()
    all_jobs.extend(wwr_jobs)
    print(f"Fetched {len(wwr_jobs)} jobs from We Work Remotely")
        
    for job in all_jobs:
        if db.is_seen(job.id):
            continue
            
        if is_target_job(job):
            print(f"🎯 Match found: {job.title} at {job.company}")
            add_to_notion(job)
            send_discord_alert(job)
            
        db.mark_seen(job.id)
        
    print("Pipeline finished.")

if __name__ == "__main__":
    main()
