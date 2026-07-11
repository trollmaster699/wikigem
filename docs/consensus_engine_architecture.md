# Consensus Engine Architecture

The Consensus Engine is the core "brain" of WikiGem. It analyzes the raw extracted data (tips) and metadata (creators) to establish truth, trust, and congruence across the fitness space.

## Proposed Strategy & Logic

The engine operates on two primary axes: **Creator Quality** and **Tip Quality**.

### 1. Consensus on Creator Quality (The "Trust Score")
To determine if a creator is a reliable source of information, we aggregate signals from multiple vectors:
*   **Peer Referencing (The Endorsement Graph):** We track which "Top Tier" (highly trusted) creators follow, mention, or collaborate with the creator. High endorsement equals high trust.
*   **Audience Sentiment (YouTube/IG Comments):** We scrape the comments of their videos and use an LLM for sentiment analysis to detect if the community generally agrees, or if there is heavy pushback (e.g., people complaining about getting injured).
*   **The "Diamond in the Rough" Discovery:** If the system detects a new, low-follower creator outputting highly unique tips that the engine verifies as *correct* (via research congruence), their trust score will rapidly inflate, and they will be automatically added to the high-priority scraping list.

### 2. Consensus on Tip Quality (The "Congruence Score")
To determine if a specific biomechanical tip is factually sound:
*   **Cross-Referencing (The Echo Chamber):** If multiple different high-trust creators all give the exact same tip (e.g., "drive your knees out on a squat"), the system flags this tip as "High Congruence / Foundational Truth".
*   **Research Paper Congruence:** We query the core concepts of a tip against actual biomechanical research. If a tip contradicts established research, it gets a "Disputed" or "Low Quality" flag.
