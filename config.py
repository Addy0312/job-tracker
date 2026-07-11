import os
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# --- Job Board Configurations ---
RSS_FEEDS = [
    "https://weworkremotely.com/categories/remote-back-end-programming-jobs.rss"
]

# --- SerpApi Google Jobs Configurations ---
# Google Jobs returns 10 results per page. 
# 1 Page = 1 API Credit.
SERPAPI_PAGES = 1 
SERPAPI_QUERY = '("C++" OR "Backend" OR "Systems") AND ("Software Engineer" OR "Developer") ("Germany" OR "Netherlands" OR "Singapore" OR "Remote")'
GOOGLE_JOBS_COOLDOWN_SECONDS = 3 * 3600  # 3 hours

KEYWORDS = [
    "c++", "backend", "systems", "linux", "networking", 
    "multithreading", "distributed systems", "stl", 
    "modern c++", "tcp/ip", "quant", "hft", "trading"
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
    # "optiver", 
    "janestreet", "robinhood"
]

LEVER_COMPANIES = [
    "palantir", 
    # "revolut", 
    # "checkoutcom"
]
