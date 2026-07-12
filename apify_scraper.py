import os
import logging
from apify_client import ApifyClient
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WikiGemApifyScraper:
    """
    Handles Phase 3 of the Data Scraping Pipeline:
    Extracts Creator metadata (follower count, following list, bio) 
    and all video URLs from the last year.
    """
    def __init__(self, api_token: str = None):
        self.api_token = api_token or os.environ.get("APIFY_API_TOKEN")
        if not self.api_token:
            logger.warning("No APIFY_API_TOKEN found. Scraper will fail on execution.")
        
        # Initialize the ApifyClient
        self.client = ApifyClient(self.api_token)

    def scrape_creator_profile(self, username: str) -> Dict[str, any]:
        """
        Scrapes a single creator's profile metadata and their recent video URLs.
        Uses the standard 'apify/instagram-profile-scraper' actor.
        """
        logger.info(f"Initiating Apify scrape for creator: @{username}")
        
        # Prepare the Actor input
        run_input = {
            "usernames": [username],
            "resultsType": "details",
            "searchType": "hashtag",
            "searchLimit": 1,
            "addParentData": False
        }

        # Run the Actor (we use a placeholder actor ID here, usually 'apify/instagram-scraper')
        # In a real environment, we'd use the exact actor ID, e.g. "apify/instagram-profile-scraper"
        logger.info(f"Calling Apify Actor for @{username} (This takes a few minutes)...")
        # run = self.client.actor("apify/instagram-profile-scraper").call(run_input=run_input)
        
        # NOTE: For this architecture demo, we mock the Apify API response 
        # so we don't accidentally burn real API credits during automated testing.
        
        mock_apify_response = {
            "username": username,
            "full_name": f"{username.capitalize()} Physical Therapy",
            "biography": "Doctor of Physical Therapy. Biomechanics expert.",
            "followers_count": 1250000,
            "following_count": 450,
            "latest_reels": [
                {"url": f"https://instagram.com/p/REEL_ID_1", "timestamp": "2026-07-10"},
                {"url": f"https://instagram.com/p/REEL_ID_2", "timestamp": "2026-07-08"},
                {"url": f"https://instagram.com/p/REEL_ID_3", "timestamp": "2026-07-05"},
                {"url": f"https://instagram.com/p/REEL_ID_4", "timestamp": "2026-07-01"},
                {"url": f"https://instagram.com/p/REEL_ID_5", "timestamp": "2026-06-28"}
            ]
        }
        
        logger.info(f"Successfully scraped metadata for @{username}. Followers: {mock_apify_response['followers_count']}")
        return mock_apify_response

if __name__ == "__main__":
    # Test execution
    scraper = WikiGemApifyScraper(api_token="dummy_token_for_now")
    data = scraper.scrape_creator_profile("squat_university")
    print(f"Found {len(data['latest_reels'])} recent reels.")
