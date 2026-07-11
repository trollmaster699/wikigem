import os
from apify_client import ApifyClient
from dotenv import load_dotenv
from database import SessionLocal
from models import Creator, Video, Category, Tip

load_dotenv()

APIFY_API_TOKEN = os.environ.get("APIFY_API_TOKEN")

def get_apify_client():
    if not APIFY_API_TOKEN:
        raise ValueError("APIFY_API_TOKEN environment variable is not set.")
    return ApifyClient(APIFY_API_TOKEN)

def scrape_creator_reels(username: str):
    """
    Scrapes the reels for a given creator and returns raw data.
    """
    client = get_apify_client()
    
    # We will use the 'apify/instagram-scraper' actor.
    run_input = {
        "usernames": [username],
        "resultsLimit": 10,  # limit for testing
        "scrapePosts": True,
    }
    
    # NOTE: Uncomment and run this when API token is set
    # run = client.actor("apify/instagram-scraper").call(run_input=run_input)
    # items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    # return items
    print(f"Would scrape {username} here with Apify.")
    return []

def save_creator_and_videos(username: str, data: list):
    """
    Process raw data and save to DB
    """
    db = SessionLocal()
    try:
        # 1. Ensure creator exists
        creator = db.query(Creator).filter(Creator.username == username).first()
        if not creator:
            creator = Creator(
                username=username,
                followers_count=0, # Parse from data if available
                endorsement_score=0,
                trust_score=0.0
            )
            db.add(creator)
            db.commit()
            db.refresh(creator)
        
        # 2. Iterate through data and save videos/tips
        for item in data:
            url = item.get("url")
            # Extract more fields...
            print(f"Processing video {url}")
            
    except Exception as e:
        print(f"Error saving to DB: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Example usage
    creator_username = "squat_university"
    data = scrape_creator_reels(creator_username)
    save_creator_and_videos(creator_username, data)
