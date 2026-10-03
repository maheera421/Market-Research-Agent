from enum import Enum

from pydantic import BaseModel


class Confidence(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class Finding(BaseModel):
    claim: str
    evidence_snippet: str
    source_url: str
    confidence: Confidence


class QueryBrief(BaseModel):
    competitor: str
    market_context: str


class RecommendationVerdict(str, Enum):
    enter = "Enter"
    dont_enter = "Don't Enter"
    enter_with_conditions = "Enter with Conditions"


class SynthesisNarrative(BaseModel):
    market_opportunity: str
    competitor_strengths_weaknesses: str
    product_gaps: str
    differentiation_strategy: str
    risks: str
    final_recommendation: RecommendationVerdict
    confidence_level: Confidence


class Recommendation(BaseModel):
    market_opportunity: str
    competitor_strengths_weaknesses: str
    product_gaps: str
    differentiation_strategy: str
    risks: str
    final_recommendation: RecommendationVerdict
    supporting_evidence: list[Finding]
    confidence_level: Confidence
