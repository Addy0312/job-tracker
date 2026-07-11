import os
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# --- Primary Targeting Configurations ---
KEYWORDS = [
    "c++", "quant", "hft", "backend", "systems", 
    "linux", "networking", "multithreading", 
    "distributed systems", "stl", "modern c++", "tcp/ip", 
    "trading"
]

ANTI_KEYWORDS = [
    "senior", "lead", "manager", "staff", 
    "principal", "director", "head", "vp"
]

LOCATIONS = [
    "germany", "berlin", "munich", "netherlands", "amsterdam", 
    "india", "bengaluru", "ireland", "dublin", "singapore", 
    "luxembourg", "switzerland", "zurich", "sweden", "stockholm", 
    "finland", "helsinki", "denmark", "remote"
]

GREENHOUSE_COMPANIES = [
    "datadog", "stripe", "cloudflare", 
    "janestreet", "robinhood"
]

LEVER_COMPANIES = [
    "palantir"
]

# --- Job Board Configurations ---
RSS_FEEDS = [
    # We Work Remotely (Backend, Fullstack, Systems)
    "https://weworkremotely.com/categories/remote-back-end-programming-jobs.rss",
    "https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss",
    "https://weworkremotely.com/categories/remote-system-administration-jobs.rss",
    # Remote.co (Developer Jobs)
    "https://remote.co/remote-jobs/developer/feed/"
]

# --- SerpApi Google Jobs Configurations ---
SERPAPI_PAGES = 1 
GOOGLE_JOBS_COOLDOWN_SECONDS = 3 * 3600  # 3 hours

# Dynamically construct the query to remain DRY.
# We slice the first 5 elements to prevent exceeding Google's 32-word query limit.
_kw_str = " OR ".join([f'"{k.title()}"' for k in KEYWORDS[:5]])
_loc_str = " OR ".join([f'"{l.title()}"' for l in LOCATIONS[:5]])
SERPAPI_QUERY = f'({_kw_str}) AND ("Software Engineer" OR "Developer" OR "Engineer") ({_loc_str})'
