import pandas as pd
import numpy as np
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from app.config import DATA_PATH, EMBEDDING_MODEL, HF_TOKEN


class SimilarityEngine:

    def __init__(self):
        # Load transformer model
        self.model = SentenceTransformer(
            EMBEDDING_MODEL,
            use_auth_token=HF_TOKEN if HF_TOKEN else None
        )

        # Load CSV
        self.titles_df = pd.read_csv(DATA_PATH)

        # Clean column names
        self.titles_df.columns = self.titles_df.columns.str.strip()

        # Ensure correct column exists
        if "Title Name" not in self.titles_df.columns:
            raise ValueError("CSV must contain 'Title Name' column")

        # Extract titles properly
        self.titles = (
            self.titles_df["Title Name"]
            .dropna()
            .astype(str)
            .str.strip()
            .tolist()
        )

        if not self.titles:
            raise ValueError("No titles found in 'Title Name' column.")

        # Precompute embeddings once
        self.embeddings = self.model.encode(self.titles)

    # -----------------------------------
    # TEXT NORMALIZATION
    # -----------------------------------
    def normalize(self, text: str):
        text = str(text)
        text = text.lower()
        text = text.strip()
        text = text.replace("\xa0", " ")
        text = re.sub(r"[^\w\s]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text

    # -----------------------------------
    # MAIN SIMILARITY FUNCTION
    # -----------------------------------
    def compute_similarity(self, new_title: str):

        normalized_input = self.normalize(new_title)

        # Build normalized map for exact match
        normalized_map = {
            self.normalize(original): original
            for original in self.titles
        }

        # ✅ EXACT MATCH
        if normalized_input in normalized_map:
            matched_title = normalized_map[normalized_input]
            return 1.0, [matched_title]

        # ✅ SEMANTIC SIMILARITY FALLBACK
        new_embedding = self.model.encode([new_title])
        scores = cosine_similarity(new_embedding, self.embeddings)[0]

        max_score = float(np.max(scores))

        top_indices = scores.argsort()[-3:][::-1]
        top_titles = [self.titles[i] for i in top_indices]

        return max_score, top_titles