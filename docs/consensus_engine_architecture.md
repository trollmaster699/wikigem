# Consensus Engine Architecture

The Consensus Engine is the core "brain" of WikiGem. It analyzes the raw extracted data (tips) and metadata (creators) to establish truth, trust, and congruence across the fitness space.

## Proposed Strategy & Logic

The engine operates on two primary axes: **Creator Quality** and **Tip Quality**.

### 1. Consensus on Creator Quality (The "Trust Score")
To determine if a creator is a reliable source of information, we will aggregate signals from multiple vectors:
*   **Peer Referencing (The Endorsement Graph):** We will track which "Top Tier" creators follow or mention the creator. High endorsement equals high trust.
*   **Deterministic Comment Filtering:** Before running sentiment analysis, we apply a hard filter. We only parse comments from users with verified PT keywords in their bio, or comments that explicitly use anatomical terms found in our database (e.g. "gluteus medius", "valgus"). This filters out engagement bait and bots.
*   **Audience Sentiment (LLM Analysis):** The filtered, high-quality comments are parsed by Gemini Flash to determine if the qualified community agrees with the tip or raises safety concerns.
*   **The "Diamond in the Rough" Discovery:** If a low-follower creator outputs highly unique tips verified as correct, their trust score rapidly inflates.

### 2. Consensus on Tip Quality (The "Congruence Score")
To determine if a specific biomechanical tip is factually sound:
*   **Semantic Matching (ChromaDB):** Tips are embedded as mathematical vectors to cluster semantically identical advice.
*   **Cross-Referencing (The Echo Chamber):** If multiple high-trust creators give the exact same tip, it is flagged as "High Congruence / Foundational Truth".
*   **Research Paper Congruence (RAG):** We query the core concepts against biomechanical research in our Vector DB.
*   **The Evergreen Data Loop (Proprioception):** The ultimate source of truth is the user. Via a 3D body map in the UI, users report where they felt the exercise (muscle activation vs. joint pain). The system cross-references this against the *expected* muscle activation predicted during the tip extraction. This objective feedback continuously updates the tip's Congruence Score.
