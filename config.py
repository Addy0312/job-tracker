import os
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

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
    "datadog", "stripe", "cloudflare", "optiver", 
    "janestreet", "robinhood"
]

LEVER_COMPANIES = [
    "palantir", "revolut", "checkoutcom"
]
