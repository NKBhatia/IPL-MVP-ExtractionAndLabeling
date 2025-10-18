import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model Configuration
EXTRACTION_MODEL = "gpt-4-turbo"
EMBEDDING_MODEL = "text-embedding-3-small"

# File Paths
SAMPLE_REPORTS_FILE = "data/sample_reports.jsonl"
EXTRACTED_FINDINGS_FILE = "data/extracted_findings.jsonl"
MAPPED_FINDINGS_FILE = "data/mapped_findings.jsonl"
FINDING_MODELS_FILE = "data/finding_models.json"

# Extraction System Prompt
EXTRACTION_SYSTEM_PROMPT = """You are a radiology AI assistant. Your task is to extract clinical findings from radiology reports.

For each report, identify all radiologic findings mentioned and determine if they are present or absent.

Return your response as a JSON array with the following structure:
[
  {
    "name": "finding name",
    "present": true/false
  }
]

Be thorough and capture all findings mentioned in the report, including:
- Pathological findings (masses, infarcts, hemorrhages, etc.)
- Anatomical variations
- Incidental findings
- Negative findings (explicitly stated as absent)

Return ONLY valid JSON, no additional text."""

# Mapping Configuration
SIMILARITY_THRESHOLD = 0.70  # Confidence threshold for finding model matches (0.0 to 1.0)
MAX_RESULTS_PER_FINDING = 1  # Number of top matches to return per finding