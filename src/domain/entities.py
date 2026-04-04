from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field, computed_field

class Pricing(BaseModel):
    """Token pricing in USD per 1M tokens."""
    input: float = 0.0
    output: float = 0.0

class Benchmarks(BaseModel):
    """Performance metrics from ArtificialAnalysis."""
    reasoning_score: Optional[float] = None
    coding_score: Optional[float] = None
    intelligence_score: Optional[float] = None
    speed_score: Optional[float] = None
    cost_efficiency: Optional[float] = None

class LLMModel(BaseModel):
    """
    Core Domain Entity: Unified LLM Registry Item.
    Matches the schema defined in docs/02-data-schema.md.
    """
    id: str = Field(..., description="Unique model ID from OpenRouter")
    name: str
    provider: str
    context_length: int
    pricing: Pricing
    modalities: List[str] = Field(default_factory=list)
    benchmarks: Optional[Benchmarks] = None
    last_synced: datetime = Field(default_factory=datetime.utcnow)

    # Derived Classifications (Step 5 of prompt)
    
    @computed_field
    @property
    def best_for(self) -> List[str]:
        """Categorize model based on its benchmark strengths."""
        tags = []
        if not self.benchmarks:
            return tags
            
        if (self.benchmarks.coding_score or 0) >= 90:
            tags.append("coding")
        if (self.benchmarks.reasoning_score or 0) >= 92:
            tags.append("reasoning")
        if self.context_length >= 128000 and (self.benchmarks.intelligence_score or 0) >= 80:
            tags.append("rag")
        if (self.benchmarks.speed_score or 0) >= 150:
            tags.append("real-time")
        if "image" in self.modalities and (self.benchmarks.intelligence_score or 0) >= 85:
            tags.append("multimodal")
        return tags

    @computed_field
    @property
    def cost_level(self) -> str:
        """Simple cost classification (Simplified for MVP, will be dynamic in Classifier)."""
        avg_price = (self.pricing.input + self.pricing.output) / 2
        if avg_price < 0.5: return "low"
        if avg_price < 5.0: return "mid"
        return "high"

    @computed_field
    @property
    def performance_tier(self) -> str:
        """Categorize model by intelligence tier."""
        score = (self.benchmarks.intelligence_score or 0) if self.benchmarks else 0
        if score >= 95: return "frontier"
        if score >= 85: return "high"
        if score >= 60: return "mid"
        return "low"

    @computed_field
    @property
    def efficiency_score(self) -> float:
        """Combined metric: Intelligence / Cost."""
        if not self.benchmarks or not self.benchmarks.intelligence_score or self.pricing.output <= 0:
            return 0.0
        # Formula: (Score / Cost per 1M Output Tokens)
        raw_score = self.benchmarks.intelligence_score / (self.pricing.output * 1000) # Weighting cost
        return round(min(1.0, raw_score / 100), 4) # Scaled for visibility
