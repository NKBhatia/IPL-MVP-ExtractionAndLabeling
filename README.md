# IPL-MVP-ExtractionAndLabeling
AI-assisted extraction and mapping of radiology findings

# AI-Assisted Longitudinal Monitoring of Radiologic Findings Using Common Data Elements

## Overview

This project implements an MVP (Minimum Viable Product) pipeline for extracting radiologic findings from medical reports and mapping them to standardized finding models using semantic similarity. The system uses OpenAI's GPT-4 for extraction and embeddings for intelligent matching.

**Project Goal:** Create a systematic way to track radiologic findings over time using standardized Common Data Elements (CDEs) from the [Open Imaging Data Model (OIDM)](https://www.openimagingdata.org/).

## Architecture

The pipeline consists of three main steps:

```
Raw Reports → Extract Findings → Map to Models → Review Mappings
```

### Step 0: Review Extracted Findings
Inspect the raw findings extracted from reports before mapping.

### Step 1: Extract Findings from Reports
- **Input:** `data/sample_reports.jsonl` (raw radiology reports)
- **Output:** `data/extracted_findings.jsonl` (presence/absence of findings)
- **Technology:** OpenAI GPT-4 with semantic extraction
- **Purpose:** Create a low-resolution map of radiologic findings

### Step 2: Map Findings to Standardized Models
- **Input:** Extracted findings + finding models
- **Output:** `data/mapped_findings.jsonl` (with confidence scores)
- **Technology:** OpenAI text embeddings + cosine similarity
- **Purpose:** Link extracted findings to standardized OIDM finding models

### Step 3: Review Mappings
- **Input:** `data/mapped_findings.jsonl`
- **Output:** Human-readable summary of mappings
- **Purpose:** Quality assurance and validation

## Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/NKBhatia/IPL-MVP-ExtractionAndLabeling.git
cd IPL-MVP-ExtractionAndLabeling

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Running the Pipeline

```bash
# Step 0: Review what was extracted
python step0_review_extracted.py

# Step 1: Extract findings from reports
python step1_extract.py

# Step 2: Map findings to models
python step2_map.py

# Step 3: Review the mappings
python step3_review_mappings.py
```

## Project Structure

```
IPL-MVP-ExtractionAndLabeling/
├── data/
│   ├── sample_reports.jsonl          # Input: Raw radiology reports
│   ├── finding_models.json           # Reference: OIDM finding models
│   ├── extracted_findings.jsonl      # Output: Step 1
│   ├── mapped_findings.jsonl         # Output: Step 2
│   └── results/                      # Output summaries
├── src/
│   └── schemas.py                    # Data models (Pydantic)
├── step0_review_extracted.py         # Review extraction results
├── step1_extract.py                  # Extract findings from reports
├── step2_map.py                      # Map to standardized models
├── step3_review_mappings.py          # Review mapping results
├── config.py                         # Configuration settings
├── requirements.txt                  # Python dependencies
├── .env.example                      # Environment variables template
└── README.md                         # This file
```

## Configuration

Edit `config.py` to adjust:
- LLM models (currently GPT-4 and text-embedding-3-small)
- File paths
- Extraction system prompt
- Similarity threshold (default 0.70)

## Data Flow

### Step 1: Extraction
Input report text:
```
"MRI shows acute infarction in the PICA territory with hemorrhagic conversion 
and significant mass effect causing effacement of the fourth ventricle and 
obstructive hydrocephalus."
```

Output extracted findings:
```json
[
  {"name": "pica territory infarct", "present": true},
  {"name": "hemorrhagic conversion", "present": true},
  {"name": "mass effect", "present": true},
  {"name": "hydrocephalus", "present": true}
]
```

### Step 2: Mapping
Each finding is compared against standardized models using semantic similarity:

```
Original Finding: "pica territory infarct"
↓
Embedding comparison
↓
Best Match: "pica infarction" (score: 0.778)
Status: MATCHED ✓
```

Findings scoring below the threshold (0.70) are flagged for manual review.

### Step 3: Review
Summary of all mappings with:
- Original extracted finding
- Mapped standardized model
- Confidence score
- Match rate statistics

## Results from MVP Testing

### Sample Output
8 radiology reports processed with 87 total findings extracted.

**Mapping Results:**
- ✓ Matched: 5 findings with high confidence (score ≥ 0.70)
- ⚠️ Flagged: 82 findings requiring manual review

**Key Matches:**
- "pica territory infarct" → "pica infarction" (0.778)
- "hydrocephalus" → "hydrocephalus" (0.806)
- "dilated lateral ventricles" → "asymmetrically enlarged lateral ventricles" (0.761)

**Finding Models Used:** 15 OIDM neuro finding models

## Key Features

- ✅ **Automated Extraction:** GPT-4 powered semantic extraction
- ✅ **Semantic Mapping:** Cosine similarity matching with embeddings
- ✅ **Confidence Scoring:** Each mapping includes a confidence score (0.0-1.0)
- ✅ **Threshold-based Flagging:** Scores below 0.70 flagged for review
- ✅ **Human-readable Output:** Multiple review scripts for validation
- ✅ **Modular Design:** Easy to swap in real OIDM API when available

## Technical Stack

- **Language:** Python 3.8+
- **LLM:** OpenAI GPT-4 (extraction)
- **Embeddings:** OpenAI text-embedding-3-small
- **Similarity:** Cosine similarity (numpy)
- **Data Validation:** Pydantic
- **File Format:** JSONL (JSON Lines)

## Future Enhancements

1. **API Integration:** Replace local finding models with real OIDM API endpoint
2. **FHIR Output:** Generate FHIR Observation resources for each finding
3. **Longitudinal Tracking:** Add temporal comparison across multiple studies
4. **Machine Learning:** Train custom models for domain-specific matching
5. **Database:** Store results in structured database instead of JSONL
6. **Web Interface:** Create dashboard for viewing and validating mappings
7. **Batch Processing:** Scale to thousands of reports
8. **Multi-modal:** Support imaging data alongside text reports

## Threshold Tuning

Current threshold is **0.70**. Adjust in `config.py`:
- **Lower (0.60-0.65):** More matches, higher false positive rate
- **Higher (0.75-0.80):** Fewer matches, higher false negative rate

Optimal threshold depends on your use case and validation requirements.

## Known Limitations

- Only extracts binary presence/absence of findings (no severity/size info)
- Finding models are manually curated (15 neuro models for MVP)
- Limited to neuro findings in current MVP
- No handling of negated findings (e.g., "no hemorrhage")
- Threshold is static (could be made dynamic based on finding type)

## Contributing

To add findings or improve the pipeline:

1. Add new finding models to `data/finding_models.json`
2. Update extraction prompt in `config.py` if needed
3. Run full pipeline and validate results
4. Submit results to GitHub

## References

- [Open Imaging Data Model](https://www.openimagingdata.org/)
- [FHIR Observations](https://www.hl7.org/fhir/observation.html)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [Radiology Gamuts Ontology](https://gamuts.net/)

## License

MIT License - feel free to use and modify for research purposes.

## Contact

For questions or feedback, reach out via GitHub issues or contact the project author.

---

**Last Updated:** October 2025
**Status:** MVP - Active Development
