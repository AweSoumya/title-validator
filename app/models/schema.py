from pydantic import BaseModel

class TitleRequest(BaseModel):
    title: str

class TitleResponse(BaseModel):
    similarity_score: float
    rule_score: float
    approval_probability: float
    final_decision: str
    confidence: str
    similar_titles: list