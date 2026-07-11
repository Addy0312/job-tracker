from models import Job
from config import KEYWORDS, ANTI_KEYWORDS, LOCATIONS

def is_target_job(job: Job) -> bool:
    title_lower = job.title.lower()
    location_lower = job.location.lower()

    # 1. Anti-keywords Check: discard if ANY anti-keyword is in the title
    if any(anti in title_lower for anti in ANTI_KEYWORDS):
        return False

    # 2. Keywords Check: discard if NO keyword is in the title
    if not any(keyword in title_lower for keyword in KEYWORDS):
        return False

    # 3. Location Check: discard if NO location matches the job location string
    if not any(loc in location_lower for loc in LOCATIONS):
        return False

    # Survives all checks
    return True
