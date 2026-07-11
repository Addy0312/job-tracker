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
    "trading", "software engineer", "developer", "platform",
    "infrastructure", "algorithm", "researcher",
    "data scientist", "data analyst", "business analyst", "consultant",
    "machine learning", "ml", "ai", "quantitative researcher"
]

ANTI_KEYWORDS = [
    # Seniority
    "senior", "lead", "manager", "staff", "principal", "director", "head", "vp",
    # Frontend / Mobile
    "frontend", "front-end", "ui", "ux", "react", "angular", "vue", "javascript",
    "ios", "android", "mobile", "fullstack", "full-stack", "full stack",
    # Data / IT / Ops
    "qa", "test", "support", "helpdesk", "administrator",
    # Non-Tech
    "sales", "marketing", "hr", "recruiter", "accountant", "legal", "finance"
]

LOCATIONS = [
    "germany", "berlin", "munich", "netherlands", "amsterdam", 
    "india", "bengaluru", "ireland", "dublin", "singapore", 
    "luxembourg", "switzerland", "zurich", "sweden", "stockholm", 
    "finland", "helsinki", "denmark", "norway", "remote",
    "uk", "london", "united kingdom", "emea", "europe", "anywhere", "global"
]

# --- Massive Free ATS Targets ---
GREENHOUSE_COMPANIES = [
    # Standard Slugs
    "datadog", "stripe", "cloudflare", "janestreet", "robinhood",
    "mongodb", "grafanalabs", "cockroachlabs", "singlestore", 
    "flowtraders", "towerresearchcapital", "akunacapital",
    # Hidden/Custom Slugs
    "wehrtyou",                   # Hudson River Trading
    "drweng",                     # DRW
    "mavensecuritiesholdingltd",  # Maven Securities
    "clickhouse"                  # ClickHouse
]

LEVER_COMPANIES = [
    "palantir" 
    # Removed: Wise, Klarna, G-Research (Custom/Workday)
]

ASHBY_COMPANIES = [
    "redis", "confluent"
]

# --- Job Board Configurations ---
RSS_FEEDS = [
    # We Work Remotely
    {"name": "WWR Backend", "url": "https://weworkremotely.com/categories/remote-back-end-programming-jobs.rss"},
    {"name": "WWR Fullstack", "url": "https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss"},
    {"name": "WWR SysAdmin", "url": "https://weworkremotely.com/categories/remote-system-administration-jobs.rss"}
]

# --- SerpApi Google Jobs Regional Aggregation ---
# Budget: 250 credits/mo. 4 searches * 2 runs/day = 240 credits/mo.
SERPAPI_PAGES = 1 
GOOGLE_JOBS_COOLDOWN_SECONDS = 12 * 3600  # 12 hours

_kw_str = " OR ".join([f'"{k.title()}"' for k in KEYWORDS[:4]])
_base_query = f'({_kw_str}) AND ("Software Engineer" OR "Developer")'

SERPAPI_SEARCHES = [
    {
        "name": "Nordics & Baltics",
        "query": f'{_base_query} ("Sweden" OR "Finland" OR "Denmark" OR "Norway" OR "Estonia")',
        "gl": "se" # Geo-target Sweden
    },
    {
        "name": "Central Europe",
        "query": f'{_base_query} ("Belgium" OR "Austria" OR "Poland" OR "Czech Republic" OR "Luxembourg")',
        "gl": "pl" # Geo-target Poland
    },
    {
        "name": "Ireland & UK",
        "query": f'{_base_query} ("Ireland" OR "Dublin" OR "London")',
        "gl": "ie" # Geo-target Ireland
    },
    {
        "name": "Asia",
        "query": f'{_base_query} ("Singapore" OR "India" OR "Bengaluru")',
        "gl": "sg" # Geo-target Singapore
    }
]
