import logging
import json
from typing import List, Dict

# Assuming models.py exists on this branch from earlier setup
from models import Video, Tip, Category, Creator
from database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DemoExtractorPipeline:
    """
    Executes Phase 4 of the Data Scraping Pipeline: The 5-Video Extraction Demo.
    Downloads videos, extracts transcripts, feeds them to Gemini, and saves to DB.
    """
    def __init__(self):
        self.db = SessionLocal()

    def run_5_video_demo(self, creator_username: str, video_urls: List[str]):
        """
        Takes exactly 5 video URLs, processes them, and commits the extracted tips to SQLite.
        """
        logger.info(f"Starting 5-Video Extraction Demo for @{creator_username}")
        
        # 1. Ensure creator exists in DB
        creator = self.db.query(Creator).filter_by(username=creator_username).first()
        if not creator:
            creator = Creator(username=creator_username, trust_score=50.0)
            self.db.add(creator)
            self.db.commit()
            
        demo_urls = video_urls[:5] # Strictly limit to 5
        
        for url in demo_urls:
            # Step A: Download Video & Transcript (Mocked for demo)
            logger.info(f"Downloading video & transcript from {url}...")
            raw_video_path, transcript = self._download_and_transcribe(url)
            
            # Step B: Run through Antigravity Ultra (Gemini)
            logger.info(f"Running {raw_video_path} through Gemini extraction...")
            extracted_data = self._run_gemini_extraction(raw_video_path, transcript)
            
            # Step C: Save to Database
            self._save_to_database(creator.id, url, extracted_data)
            
        logger.info("Demo Extraction Complete. All 5 videos processed and saved to SQLite.")

    def _download_and_transcribe(self, url: str):
        # Placeholder: Uses yt-dlp to grab the actual mp4 and auto-generated captions
        return ("/tmp/video_mock.mp4", "Here is exactly how you fix tight ankles for squats...")

    def _run_gemini_extraction(self, video_path: str, transcript: str) -> List[Dict]:
        """
        Calls the Gemini API via Antigravity Ultra SDK. 
        Prompts it to output strictly structured JSON based on our schema.
        """
        # Mocking the JSON output that Gemini would return
        return [
            {
                "tip_summary": "Elevate heels for deep squats",
                "main_category": "mobility",
                "individual_tip": "If you lack ankle dorsiflexion, elevating your heels allows the knees to track forward without lifting the heel, maintaining proper spinal posture.",
                "body_area": "ankles",
                "muscles_targeted": "calves"
            }
        ]

    def _save_to_database(self, creator_id: int, url: str, extracted_tips: List[Dict]):
        """
        Maps the JSON output from Gemini to our SQLAlchemy models and commits.
        """
        # 1. Create Video Record
        video = Video(url=url, creator_id=creator_id)
        self.db.add(video)
        self.db.flush() # Get video ID
        
        # 2. Iterate through extracted tips
        for tip_data in extracted_tips:
            # Find or create category
            cat_name = tip_data['main_category'].lower()
            category = self.db.query(Category).filter_by(name=cat_name).first()
            if not category:
                category = Category(name=cat_name)
                self.db.add(category)
                self.db.flush()
                
            # Create Tip Record
            new_tip = Tip(
                content=tip_data['individual_tip'],
                category_id=category.id,
                video_id=video.id,
                body_area=tip_data['body_area'],
                muscles_targeted=tip_data['muscles_targeted'],
                congruence_score=50.0 # Baseline score before Consensus Engine runs
            )
            self.db.add(new_tip)
            
        self.db.commit()
        logger.info(f"Saved {len(extracted_tips)} tips from {url} into DB.")

if __name__ == "__main__":
    demo = DemoExtractorPipeline()
    test_urls = [
        "https://instagram.com/p/1", "https://instagram.com/p/2", 
        "https://instagram.com/p/3", "https://instagram.com/p/4", 
        "https://instagram.com/p/5"
    ]
    demo.run_5_video_demo("squat_university", test_urls)
