# Instagram Reels Scraper & Database Schema

We will build a Python-based application to scrape Instagram reels from specific creators in the fitness space and store the structured data in a relational database. 

## Proposed Technology Stack
* **Language:** Python
* **Database:** SQLite (easiest for local development and starting out, can easily migrate to PostgreSQL later)
* **ORM (Object Relational Mapper):** SQLAlchemy (allows defining DB models in Python)
* **Scraping:** We recommend using a third-party API like **Apify (Instagram Scraper)**. It is highly robust, manages proxies, login sessions, and rate-limits for you. An alternative is **RapidAPI (e.g., RocketAPI)** for simpler REST queries. We will set up the scraper to pull data using Apify's API.
* **Extraction (Optional next step):** Using an LLM (like Gemini or OpenAI) to automatically categorize videos and extract specific tips/muscles from the caption or video transcript.

## Database Schema Design

### 1. `Creator` Table
* `id`: Primary Key
* `username`: String (Unique)
* `followers_count`: Integer
* `endorsement_score`: Integer (Placeholder for now, representing the number of trusted creators following them)
* `trust_score`: Integer/Float (Logic for this will be implemented later)

### 2. `Video` Table
* `id`: Primary Key
* `creator_id`: Foreign Key linking to `Creator`
* `url`: String (Unique link to the Instagram reel)
* `summary`: String (A short description of what the video is about)
* `categories`: List of Enum/String (A video can have multiple categories. Restricted to: `posture`, `pain-correction-muscle imbalance`, `hypertrophy`, `explosiveness and athleticism`, `sports performance`. We will use an association table `VideoCategory` to handle this many-to-many relationship)

### 3. `Tip` Table (One Video can have multiple Tips)
* `id`: Primary Key
* `video_id`: Foreign Key linking to `Video`
* `content`: Text (An individual tip from the video)
* `category`: String (More granular category inspired by the video category, e.g., 'setup', 'execution', 'common mistake')
* `body_area`: String (The specific body part being worked on, e.g., 'lower back', 'shoulders')
* `target_muscles`: String/List (The list of muscles, e.g., 'gluteus maximus', 'hamstrings')

## Proposed Changes
### Backend / Scraping Pipeline
#### [NEW] `models.py`
Will contain the SQLAlchemy definitions for `Creator`, `Video`, and `Tip`.
#### [NEW] `scraper.py`
The script responsible for fetching a given creator's reels and saving raw data.
#### [NEW] `database.py`
Utility to initialize the SQLite database and handle connections/sessions.
#### [NEW] `requirements.txt`
Will list the Python dependencies (e.g., `sqlalchemy`, `instaloader`).

> [!IMPORTANT] 
> We will use Apify for scraping as it handles rate limits and authentication out-of-the-box, ensuring higher resilience. You will need an Apify API key.

## Decisions Made
1. **Extraction:** We will use **Whisper** for audio extraction/transcription in addition to using the video captions. This will allow for much richer analysis and tip generation.
2. **Tech Stack:** Python + SQLite + SQLAlchemy is approved.
3. **Categories:** Tip categories will be generated **dynamically** for now using an LLM. Later, we will analyze the generated data to establish common categories and determine the best way to categorize them systematically.
