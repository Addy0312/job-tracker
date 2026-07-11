import time
import concurrent.futures
from config import GREENHOUSE_COMPANIES, LEVER_COMPANIES, GOOGLE_JOBS_COOLDOWN_SECONDS, SERPAPI_SEARCHES
from fetchers import fetch_greenhouse_jobs, fetch_lever_jobs, fetch_hn_jobs, fetch_wwr_jobs, fetch_google_jobs, fetch_remoteok_jobs, fetch_arbeitnow_jobs
from filters import is_target_job
from integrations import add_to_notion, send_discord_alert
from db import JobDatabase

def main():
    print("Starting Job Sourcing Pipeline (Parallel Mode)...")
    db = JobDatabase()
    all_jobs = []
    
    # 1. Fetch all jobs in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        future_to_name = {}
        
        # Queue Greenhouse companies
        for company in GREENHOUSE_COMPANIES:
            future = executor.submit(fetch_greenhouse_jobs, company)
            future_to_name[future] = f"Greenhouse: {company}"
            
        # Queue Lever companies
        for company in LEVER_COMPANIES:
            future = executor.submit(fetch_lever_jobs, company)
            future_to_name[future] = f"Lever: {company}"
            
        # Queue Hacker News
        future = executor.submit(fetch_hn_jobs)
        future_to_name[future] = "Hacker News"
        
        # Queue RSS Feeds (We Work Remotely, Remote.co)
        future = executor.submit(fetch_wwr_jobs)
        future_to_name[future] = "RSS Feeds"
        
        # Queue Remote OK
        future = executor.submit(fetch_remoteok_jobs)
        future_to_name[future] = "Remote OK"
        
        # Queue Arbeitnow (Germany / EU)
        future = executor.submit(fetch_arbeitnow_jobs)
        future_to_name[future] = "Arbeitnow (Germany)"
        
        # Queue Google Jobs (Regional Grouped Searches)
        last_google_run = db.get_meta("google_jobs_last_run")
        current_time = time.time()
        
        if last_google_run and (current_time - float(last_google_run)) < GOOGLE_JOBS_COOLDOWN_SECONDS:
            hours_left = round((GOOGLE_JOBS_COOLDOWN_SECONDS - (current_time - float(last_google_run))) / 3600, 1)
            print(f"Skipping Google Jobs: Cooldown active ({hours_left} hours remaining).")
        else:
            for search_config in SERPAPI_SEARCHES:
                future = executor.submit(fetch_google_jobs, search_config)
                future_to_name[future] = f"Google Jobs ({search_config['name']})"
            db.set_meta("google_jobs_last_run", str(current_time))
            
        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_name):
            name = future_to_name[future]
            try:
                jobs = future.result()
                all_jobs.extend(jobs)
                print(f"Fetched {len(jobs):<4} jobs from {name}")
            except Exception as exc:
                print(f"Error fetching from {name}: {exc}")
                
    # 2. Filter and Push matches sequentially (to respect Notion API limits)
    print(f"\nProcessing {len(all_jobs)} total jobs...")
    matches_found = 0
    
    for job in all_jobs:
        if db.is_seen(job.id):
            continue
            
        if is_target_job(job):
            print(f"🎯 Match found: {job.title} at {job.company}")
            add_to_notion(job)
            send_discord_alert(job)
            matches_found += 1
            
        db.mark_seen(job.id)
        
    print(f"Pipeline finished. Forwarded {matches_found} new matches.")

if __name__ == "__main__":
    main()
