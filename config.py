import os
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# --- Primary Targeting Configurations ---
KEYWORDS = [
    "data analyst", "business analyst", "finance analyst", 
    "associate consultant", "business development executive", 
    "business development associate", "business associate", 
    "business intelligence", "bi developer",
    "analytics", "strategy", "operations", "data science",
    "consultant", "management consultant"
]

ANTI_KEYWORDS = [
    # Seniority
    "senior", "lead", "manager", "staff", "principal", "director", "head", "vp",
    # Software Engineering / Tech
    "software", "software engineering", "software engineer", "frontend", "front-end", 
    "ui", "ux", "react", "angular", "vue", "javascript", "ios", "android", "mobile", 
    "fullstack", "full-stack", "full stack", "backend", "devops", "c++", "java", 
    "python developer", "systems engineer", "sre", "cloud engineer",
    # Data / IT / Ops
    "qa", "test", "support", "helpdesk", "administrator", "it"
]

LOCATIONS = [
    "india", "bengaluru", "bangalore", "mumbai", "gurgaon", "noida", 
    "hyderabad", "pune",
    "remote", "singapore", "london", "new york", "ny", "nyc"
]

# --- Massive Free ATS Targets ---
# Note: The following companies were removed as they moved to internal ATS or closed public API access:
# uber, doordash, razorpay, swiggy, bharatpe, cleartax, browserstack, chargebee, khatabook, checkoutcom, 
# spinny, cars24, flipkart, canva, myntra, klarna, revolut, zomato, zepto, upstox, rippling
GREENHOUSE_COMPANIES = [
    "stripe", "groww", "airbnb", "instacart", "coinbase", "brex", "gusto", "block", # block = square
    "adyen", "postman", "zenoti", "lyft", "phonepe", "monzo", "n26", "slice", 
    "chime", "affirm", "robinhood", "remote", "figma"
]

LEVER_COMPANIES = [
    "kraken", "plaid", "wealthsimple", "meesho", "mindtickle", "paytm", "cred", "binance"
]

ASHBY_COMPANIES = [
    "navi", "pliant", "deel", "oyster", "notion", "ramp"
]

# --- Job Board Configurations ---
RSS_FEEDS = [
    {"name": "WWR Management & Finance", "url": "https://weworkremotely.com/categories/remote-management-and-finance-jobs.rss"},
    {"name": "WWR Sales & Marketing", "url": "https://weworkremotely.com/categories/remote-sales-and-marketing-jobs.rss"},
    {"name": "WWR Product", "url": "https://weworkremotely.com/categories/remote-product-jobs.rss"}
]

# --- SerpApi Google Jobs Regional Aggregation ---
# Budget: 250 credits/mo. 4 searches * 2 runs/day = 240 credits/mo.
SERPAPI_PAGES = 1 
GOOGLE_JOBS_COOLDOWN_SECONDS = 12 * 3600  # 12 hours

_roles = '("Data Analyst" OR "Business Analyst" OR "Consultant" OR "Finance Analyst" OR "Strategy" OR "Operations")'
_big_banks_consultancies = '("JPMorgan" OR "Citi" OR "Citicorp" OR "Deloitte" OR "EY" OR "Ernst & Young" OR "ZS Associates" OR "Goldman Sachs" OR "Morgan Stanley" OR "PwC" OR "KPMG")'
_indian_fintech = '("Myntra" OR "PhonePe" OR "Razorpay" OR "Cred" OR "Groww" OR "Khatabook" OR "Stripe" OR "Checkout.com" OR "Swiggy" OR "Zomato" OR "Zepto" OR "Meesho" OR "BharatPe" OR "Upstox" OR "Slice" OR "Navi" OR "Paytm")'
_global_remote = '("Remote" OR "Anywhere")'

SERPAPI_SEARCHES = [
    {
        "name": "Big Banks & Consultancies in India",
        "query": f'{_roles} AND {_big_banks_consultancies}',
        "gl": "in"
    },
    {
        "name": "Big Banks & Consultancies Global/US",
        "query": f'{_roles} AND {_big_banks_consultancies}',
        "gl": "us"
    },
    {
        "name": "Indian Fintech & E-Commerce",
        "query": f'{_roles} AND {_indian_fintech}',
        "gl": "in"
    },
    {
        "name": "Global Remote Business/Data Roles",
        "query": f'{_roles} AND {_global_remote}',
        "gl": "us"
    }
]
