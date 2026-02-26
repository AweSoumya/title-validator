import re

class RuleEngine:

    def evaluate(self, title: str):

        score = 1.0

        if len(title) < 5 or len(title) > 100:
            score -= 0.3

        words = title.split()
        if len(set(words)) / len(words) < 0.6:
            score -= 0.2

        if re.search(r"(.)\1{3,}", title):
            score -= 0.2

        if any(char.isdigit() for char in title):
            score -= 0.1

        return max(score, 0.0)