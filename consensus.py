import math
import logging
from typing import List, Dict

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConsensusEngine:
    """
    The core engine responsible for calculating Creator Quality (Trust Score)
    and Tip Quality (Congruence Score).
    """

    def __init__(self, db_session, vector_store):
        """
        Initializes the Consensus Engine.
        :param db_session: SQLAlchemy database session
        :param vector_store: ChromaDB vector store client
        """
        self.db = db_session
        self.vector_store = vector_store

    def calculate_trust_score(self, creator_id: int) -> float:
        """
        Calculates the Trust Score for a creator based on:
        1. Peer Referencing (Endorsement Graph)
        2. Audience Sentiment (via Deterministic Filtering + LLM)
        3. Diamond in the Rough detection
        """
        logger.info(f"Calculating Trust Score for creator {creator_id}")
        
        # 1. Base Score from Endorsements
        # In a real scenario, this queries the creator_endorsements table
        endorsement_score = self._get_endorsement_score(creator_id)
        
        # 2. Sentiment Score from Comments
        # Fetches only deterministically filtered comments (PT keywords/anatomy terms)
        sentiment_score = self._get_comment_sentiment_score(creator_id)
        
        # Calculate weighted average
        # Endorsements are heavily weighted (e.g., 70%), Sentiment is (30%)
        trust_score = (endorsement_score * 0.7) + (sentiment_score * 0.3)
        
        # TODO: Add logic for "Diamond in the Rough" inflation
        
        return round(trust_score, 2)

    def calculate_congruence_score(self, tip_id: int) -> float:
        """
        Calculates the Congruence Score for a specific tip based on:
        1. Semantic Echo Chamber (Are other high-trust creators saying this?)
        2. RAG Research Paper alignment
        3. Evergreen Data Loop (User Proprioception & Form Verification)
        """
        logger.info(f"Calculating Congruence Score for tip {tip_id}")
        
        # 1. Check Semantic Echo Chamber via ChromaDB
        # Find similar tips and average the trust scores of their creators
        echo_score = self._get_semantic_echo_score(tip_id)
        
        # 2. RAG Alignment
        research_score = self._check_research_congruence(tip_id)
        
        # 3. Evergreen User Proprioception Feedback
        # If users followed form (MediaPose) but got pain/no activation, penalize heavily.
        proprioception_penalty = self._get_proprioception_penalty(tip_id)
        
        congruence_score = ((echo_score * 0.6) + (research_score * 0.4)) - proprioception_penalty
        
        # Normalize between 0 and 100
        congruence_score = max(0.0, min(100.0, congruence_score))
        
        return round(congruence_score, 2)

    # --- Private Helper Methods ---

    def _get_endorsement_score(self, creator_id: int, creator_data: Dict = None) -> float:
        """
        Calculates endorsement score based on the number and quality of incoming endorsements.
        """
        if not creator_data:
            return 50.0
            
        # Example logic: log-scale of highly trusted followers
        high_trust_followers = creator_data.get('high_trust_follower_count', 0)
        if high_trust_followers == 0:
            return 0.0
            
        # Logarithmic scale so 100 high-trust followers is near max score
        score = (math.log10(high_trust_followers + 1) / 2.0) * 100
        return min(100.0, score)

    def _get_comment_sentiment_score(self, creator_id: int, sentiment_data: Dict = None) -> float:
        """
        Calculates sentiment score from deterministically filtered comments.
        """
        if not sentiment_data:
            return 50.0
            
        positive_mentions = sentiment_data.get('positive_clinical_mentions', 0)
        negative_mentions = sentiment_data.get('negative_clinical_mentions', 0)
        
        total = positive_mentions + negative_mentions
        if total == 0:
            return 50.0 # Neutral baseline
            
        return (positive_mentions / total) * 100.0

    def _get_semantic_echo_score(self, tip_id: int, chroma_results: List[Dict] = None) -> float:
        """
        Calculates how many high-trust creators are echoing this exact tip.
        """
        if not chroma_results:
            return 50.0
            
        # Average the trust scores of the creators who echo this tip
        total_trust = sum(result.get('creator_trust_score', 0) for result in chroma_results)
        return total_trust / len(chroma_results) if chroma_results else 0.0

    def _check_research_congruence(self, tip_id: int, rag_score: float = None) -> float:
        """
        Returns the RAG alignment score (0-100) based on PubMed/Semantic Scholar.
        """
        return rag_score if rag_score is not None else 50.0

    def _get_proprioception_penalty(self, tip_id: int, feedback_data: Dict = None) -> float:
        """
        The critical feedback loop: Penalizes tips where form was perfect but 
        the user still failed activation or experienced pain.
        """
        if not feedback_data:
            return 0.0
            
        total_attempts = feedback_data.get('total_verified_attempts', 0)
        pain_reports = feedback_data.get('pain_reports', 0)
        activation_failures = feedback_data.get('activation_failures_after_prep', 0)
        
        if total_attempts == 0:
            return 0.0
            
        failure_rate = (pain_reports + activation_failures) / total_attempts
        
        # Heavy penalty: A 20% failure rate drops the congruence score by 40 points.
        penalty_multiplier = 200.0 
        return min(100.0, failure_rate * penalty_multiplier)

    def calculate_execution_difficulty(self, tip_id: int, execution_data: Dict = None) -> Dict[str, any]:
        """
        Calculates the global Execution Success Rate (%) for an exercise and 
        correlates failures with specific demographic or historical trends.
        """
        logger.info(f"Calculating Execution Difficulty for tip {tip_id}")
        
        if not execution_data:
            return {"global_success_rate": 0.0, "failure_trends": []}
            
        total_attempts = execution_data.get('total_attempts', 0)
        successful_attempts = execution_data.get('successful_attempts', 0)
        
        global_success_rate = (successful_attempts / total_attempts * 100.0) if total_attempts > 0 else 0.0
        
        # Calculate failure trends dynamically based on user history metadata
        failure_trends = []
        history_categories = execution_data.get('failed_user_histories', {})
        
        for condition, fail_count in history_categories.items():
            condition_total = execution_data.get('total_users_with_condition', {}).get(condition, 1)
            condition_failure_rate = (fail_count / condition_total) * 100.0
            
            # Only flag statistically significant failure trends (> 60% failure rate)
            if condition_failure_rate > 60.0:
                failure_trends.append({
                    "condition": condition,
                    "failure_rate": round(condition_failure_rate, 1)
                })
        
        return {
            "global_success_rate": round(global_success_rate, 1),
            "failure_trends": failure_trends
        }
