class DecisionEngine:

    def decide(self, similarity, rule_score, probability):

        if similarity == 1.0:
            return "REJECT", "HIGH"

        if similarity >= 0.8:
            return "REVIEW", "MEDIUM"

        return "ACCEPT", "LOW"