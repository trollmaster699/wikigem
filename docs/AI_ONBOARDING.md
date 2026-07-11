# WikiGem: AI Context & Onboarding

**CRITICAL INSTRUCTION FOR AI ASSISTANTS:**
Read this document entirely before writing code or modifying architecture. This document contains the epistemological philosophy, core engine mechanics, and branching strategy for the WikiGem project.

## 1. Project Philosophy
WikiGem is an AI-driven biomechanics and physical therapy aggregator. 
**The Golden Rule:** WikiGem is a *Librarian* and a *Curation Shield*, NOT a doctor. It does not generate medical advice. It parses, filters, and ranks advice from highly trusted creators (e.g., SquatUniversity) and transfers liability to the original video source.

**The "Slop In, Slop Out" Problem:** We assume AI vision models are terrible at extracting 3D nuance from 2D Instagram reels (lens distortion, baggy clothing). Therefore, we do NOT trust the AI's extraction as the final truth. The ultimate source of truth is the **User's Proprioception** (where they actually felt the muscle working).

## 2. Core Architecture & Engines

### A. The Consensus Engine
Calculates a Congruence Score (1-100) for every extracted tip to verify its legitimacy.
*   **Endorsement Score:** How many high-trust peers follow/endorse the creator.
*   **Semantic Echo:** Does ChromaDB find other high-trust creators saying the exact same thing?
*   **Deterministic Filtering:** Comments are filtered for specific anatomical keywords to prevent hallucinating engagement-bait.
*   **Research Congruence:** Does the tip align with RAG-queried biomechanics PDFs (PubMed/Semantic Scholar)?

### B. The Evergreen Data Loop & Diagnostic UI
A good tip can fail if the user executes it poorly. We prevent unfairly penalizing good tips via this loop:
1.  **MediaPose Form Verification:** Frontend UI uses MediaPose to ensure the user physically followed the instructions.
2.  **Activation Prescriptions:** If form is correct but the target muscle is not felt, the system prescribes a specific *Activation Exercise* (e.g., glute bridges).
3.  **The Penalty:** A tip is only penalized in the database if form is perfect, activation is done, and it *still* causes pain.

### C. Execution Difficulty & Failure Trend Analysis
The system tracks the **Execution Success Rate** of every exercise. If failures occur, the system correlates them across three metadata axes:
*   **Body Geometry:** (e.g., Long femurs)
*   **Mobility Constraints:** (e.g., Tight ankles)
*   **Medical History:** (e.g., Previous hamstring tear)

### D. The Diagnostic Decoding Engine (The A/B Tester)
When a high failure trend is detected (e.g., "80% of users with long femurs fail squats"), the engine attempts to "cure" it. It hypothesizes cures by:
1.  Finding historically successful activation exercises for that demographic.
2.  Querying ChromaDB for tips that specifically mention the failure condition (e.g., "Elevate heels if you have long femurs").
It serves these cures and tracks if the success rate improves.

### E. Data Source Discovery ("Diamond in the Rough")
Scans YouTube/IG comments for mentions of unknown creators. It runs a shallow scrape of their videos and evaluates them against the Consensus Engine. If they output highly unique but factually correct tips (high research congruence, low semantic echo), their Trust Score is artificially inflated and they are added to the priority scraping queue.

## 3. Tech Stack & Repository Structure
*   **Backend:** Python, SQLAlchemy (SQLite for relational data), ChromaDB (Vector store for semantic search and RAG).
*   **Data Extraction:** Antigravity Ultra (Native AI parsing, avoiding complex 3rd party API wrappers).
*   **Frontend (Planned):** MediaPose for body tracking, 3D Body Map UI for proprioception feedback.

### Branching Strategy (DO NOT MERGE UNLESS INSTRUCTED)
*   `main`: The source of truth for documentation and verified code.
*   `feature/ai-tip-extraction`: Multimodal extraction and DB timestamping.
*   `feature/consensus-engine`: Core mathematical logic for congruence scoring, failure trends, and the diagnostic decoding engine. Includes `feedback_models.py`.
*   `feature/data-source-discovery`: Crawling logic (`discovery.py`) for finding new creators.
*   `feature/diagnostic-ui`: Frontend logic for MediaPose and the 3D Body Map.

**FINAL CRITICAL RULE TO AI: THE SYNCHRONIZATION MANDATE**
Whenever you make ANY update to the project's logic, architecture, or write new code on a feature branch, you MUST update the documentation (`AI_ONBOARDING.md`, `README.md`, or architecture docs). Furthermore, you must explicitly run Git commands to synchronize these document updates across ALL active branches immediately. The documentation must remain perfectly identical across the entire repository at all times, regardless of branch.
