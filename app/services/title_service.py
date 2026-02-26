from app.core.similarity import SimilarityEngine
from app.core.rules import RuleEngine
from app.core.probability import ProbabilityEngine
from app.core.decision import DecisionEngine


class TitleService:

    def __init__(self):
        self.sim_engine = SimilarityEngine()
        self.rule_engine = RuleEngine()
        self.prob_engine = ProbabilityEngine()
        self.decision_engine = DecisionEngine()

    def analyze(self, title):

        similarity_score, similar_titles = self.sim_engine.compute_similarity(title)
        rule_score = self.rule_engine.evaluate(title)
        probability = self.prob_engine.predict_probability(similarity_score)
        decision, confidence = self.decision_engine.decide(
            similarity_score,
            rule_score,
            probability
        )

        # Convert similarity to percentage for reasoning
        similarity_percent = similarity_score * 100

        # Generate meaningful remarks
        if similarity_percent < 30:
            reason = "No significantly similar registered title found."
        elif similarity_percent < 70:
            reason = "Moderate similarity detected. Manual review recommended."
        else:
            if similar_titles:
                reason = f"High similarity detected with: {', '.join(similar_titles[:3])}"
            else:
                reason = "High similarity detected with an existing registered title."

        return {
            "similarity_score": round(similarity_score, 3),
            "verification_probability": round(probability, 3),  # renamed for frontend
            "rule_score": round(rule_score, 3),
            "final_decision": decision,
            "confidence": confidence,
            "similar_titles": similar_titles,
            "reason": reason
        }