class ProbabilityEngine:

    def predict_probability(self, similarity_score: float) -> float:
        """
        Inverse proportional logic:
        Higher similarity → Lower approval probability
        """

        probability = 1.0 - similarity_score

        probability = max(0.0, min(1.0, probability))

        return probability