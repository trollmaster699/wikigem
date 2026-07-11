# Consensus Engine Architecture

The Consensus Engine is the core "brain" of WikiGem. It analyzes the raw extracted data (tips) and metadata (creators) to establish truth, trust, and congruence across the fitness space.

## Proposed Strategy & Logic

The engine operates on two primary axes: **Creator Quality** and **Tip Quality**.

### 1. Consensus on Creator Quality (The "Trust Score")
To determine if a creator is a reliable source of information, we aggregate signals from multiple vectors:
*   **Peer Referencing (The Endorsement Graph):** We track which "Top Tier" (highly trusted) creators follow, mention, or collaborate with the creator. High endorsement equals high trust.
*   **Audience Sentiment (YouTube/IG Comments):** We will scrape the comments of individual videos to run sentiment analysis on specific *tips*. This tells us if the community generally agrees or if there is pushback for a specific exercise (e.g., people complaining about getting injured). Furthermore, comments on individual videos often act as a vector for **Data Source Discovery**, because users frequently mention other creators or videos that provide better alternatives. We can scrape these mentions to find new creators to add to the system.
*   **The "Diamond in the Rough" Discovery:** If the system detects a new, low-follower creator outputting highly unique tips that the engine verifies as *correct* (via research congruence), their trust score will rapidly inflate, and they will be automatically added to the high-priority scraping list.

### 2. Consensus on Tip Quality (The "Congruence Score")
To determine if a specific biomechanical tip is factually sound:
*   **Semantic Matching (ChromaDB):** Tips are embedded as mathematical vectors and stored in a local **ChromaDB**. This allows the engine to instantly cluster tips that are semantically identical (e.g. "push knees out" vs "drive knees outward") even if the words are different.
*   **Cross-Referencing (The Echo Chamber):** If multiple different high-trust creators all give the exact same tip, the system flags this tip cluster as "High Congruence / Foundational Truth".
*   **Research Paper Congruence (RAG):** We query the core concepts of a tip against actual biomechanical research stored in our Vector DB. If a tip contradicts established research, it gets a "Disputed" or "Low Quality" flag.
