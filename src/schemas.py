from typing import List, Optional
from pydantic import BaseModel, Field


class Finding(BaseModel):
    """A single extracted radiological finding."""
    name: str = Field(..., description="Lowercase finding name")
    present: bool = Field(..., description="True if present, False if absent")


class ExtractionResult(BaseModel):
    """Results from step 1: extracting findings from a report."""
    report_id: str
    findings: List[Finding]


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