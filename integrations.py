import requests
from datetime import datetime
from notion_client import Client
from models import Job
from config import NOTION_TOKEN, NOTION_DATABASE_ID, DISCORD_WEBHOOK_URL

def add_to_notion(job: Job):
    if not NOTION_TOKEN or not NOTION_DATABASE_ID:
        print("Warning: NOTION_TOKEN or NOTION_DATABASE_ID is not set. Skipping Notion integration.")
        return
    
    try:
        notion = Client(auth=NOTION_TOKEN)
        properties = {
            "Company": {"title": [{"text": {"content": job.company}}]},
            "Role": {"rich_text": [{"text": {"content": job.title}}]},
            "Location": {"rich_text": [{"text": {"content": job.location}}]},
            "Link": {"url": job.url},
            "Date": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
            "Status": {"select": {"name": "To Apply"}},
            "Source": {"select": {"name": job.source}}
        }
        
        notion.pages.create(
            parent={"database_id": NOTION_DATABASE_ID},
            properties=properties
        )
    except Exception as e:
        print(f"Error adding to Notion: {e}")

def send_discord_alert(job: Job):
    if not DISCORD_WEBHOOK_URL:
        print("Warning: DISCORD_WEBHOOK_URL is not set. Skipping Discord alert.")
        return
    
    content = (
        f"🚨 **New Job Match!** 🚨\n"
        f"**Company:** {job.company}\n"
        f"**Role:** {job.title}\n"
        f"**Location:** {job.location}\n"
        f"**Apply:** {job.url}"
    )
    
    try:
        requests.post(
            DISCORD_WEBHOOK_URL, 
            json={"content": content}, 
            timeout=10
        )
    except Exception as e:
        print(f"Error sending Discord alert: {e}")
