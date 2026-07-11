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
*   **The Evergreen Data Loop (Form Verification & Activation):** The ultimate source of truth is the user. Via a 3D body map in the UI, users report where they felt the exercise (muscle activation vs. joint pain). To prevent unfairly penalizing a good tip due to bad user form:
    1. **MediaPose Verification:** The frontend UI uses MediaPose to ensure the user actually followed the tip.
    2. **Activation Exercises:** If form is correct but the target muscle wasn't felt, the system prescribes a specific *activation exercise* (e.g., glute bridges). 
    3. **Tip Downgrade:** A tip's Congruence Score is only penalized if form was perfect, activation was done, and it *still* failed. If an exercise consistently requires an activation set to work, the system links them in the database to always serve the activation exercise first.
    4. **Execution Difficulty (Success Rate):** We calculate the global % of users who can successfully execute the movement.
    5. **Failure Trend Analysis:** We correlate failure rates with specific demographic/historical trends (e.g., "82% of users with prior ankle sprains fail this"). This data comes from user profiles and caveats parsed from the original video.
    6. **Diagnostic Decoding Engine:** The system actively attempts to "cure" trends. If people with long femurs fail squats, the engine tests variables by prescribing activation exercises or finding specific creator tips that address this (e.g., "elevate heels"). It tracks which intervention successfully neutralizes the failure trend over time.

*   **The "Critic" Agent (Anti-Hallucination Layer):** The primary LLM is never allowed to output directly to the user. All outputs pass through an invisible "Critic Agent" whose sole job is to cross-reference the output against the retrieved consensus and research vectors. If a hallucination is detected, the Critic kills the output and triggers a re-query.
*   **Grounding to Truth:** Every single recommendation presented to the user MUST have a `source_id` explicitly tied to a verified video or research paper. If the engine cannot attach a `source_id` to a concept, it is strictly programmed to say: "I don't have enough consensus data on this," rather than attempting to guess.
