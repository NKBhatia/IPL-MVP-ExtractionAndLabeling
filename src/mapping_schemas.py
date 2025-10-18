from typing import List, Optional
from pydantic import BaseModel, Field


class MappedFinding(BaseModel):
    """A single finding mapped to a finding model."""
    extracted_finding_name: str
    present: bool
    matched_finding_model_id: Optional[str] = None
    matched_finding_model_name: Optional[str] = None
    confidence_score: float
    status: str


class MappingResult(BaseModel):
    """Results from step 2: mapping findings to models."""
    report_id: str
    mappings: List[MappedFinding]