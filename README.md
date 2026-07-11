# WikiGem 💎

Welcome to the **WikiGem** repository! This is the core repository for building an AI-driven system that aggregates fitness, rehab, and biomechanical content from various sources (Instagram, YouTube, etc.) and processes it using a "congruence engine" to synthesize training advice.

## System Architecture & Branching Guide

This project is modular, and different parts of the system are developed in separate feature branches before they are stable enough to merge into `main`.

If you are developing a new component, **check below** to see if an active branch already exists for it, or if you should create a new one.

### Current Active Branches

*   **`feature/instagram-reels-scraper`**
    *   **Status:** 🚧 In Progress
    *   **Purpose:** Building the pipeline to scrape Instagram Reels from fitness creators using Apify and transcribe them using Whisper. Also contains the initial foundational SQLite database schema (`Creator`, `Video`, `Tip`).
    *   **Action:** If you are working on the database models, Instagram scraping, or Whisper transcription, checkout this branch!

### Planned / Future Modules (Need New Branches)

If you are starting work on any of the following, please create a **new branch** off of `main`:

*   **`feature/youtube-scraper`**: For scraping YouTube videos and playlists from purchased courses or channels.
*   **`feature/congruence-engine`**: For the AI logic that cross-references and synthesizes the tips stored in the database to find congruence (or conflicting advice) across creators.
*   **`feature/diagnostic-ui`**: For building the frontend UI that users interact with to get their weekly training program.

## Documentation

Each feature branch contains its own detailed documentation within the `docs/` folder (e.g., `docs/instagram_scraper_architecture.md`). Once a branch is merged into `main`, its documentation will also become available here on the main branch, creating a comprehensive, interconnected Wiki.

## How to Contribute

1.  Check the "Current Active Branches" list above.
2.  Checkout an existing branch or create a new one from `main` (e.g., `git checkout -b feature/your-feature-name`).
3.  Ensure you document major architectural decisions in the `docs/` folder of your branch.
