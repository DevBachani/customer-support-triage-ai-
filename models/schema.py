from pydantic import BaseModel, Field
from typing import Optional
import config

class TriageResult(BaseModel):
    category: str = Field(description="Must exactly match one of the predefined categories.")
    priority: str = Field(description="Must be exactly P0, P1, P2, or P3.")
    summary: str = Field(min_length=10, description="A concise summary of the customer's issue.")
    suggested_action: str = Field(min_length=10, description="What the agent should do next.")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0.")
    needs_human: bool = Field(description="True if confidence is low or escalation rules are met.")
    escalation_reason: Optional[str] = Field(default=None, description="Why this needs human review, if applicable.")