import json
import os
from pathlib import Path
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from src.schemas import ExtractionResult, Finding
import config

# Initialize Pydantic AI agent with your Finding schema and retry logic
agent = Agent(
    model=OpenAIModel(config.EXTRACTION_MODEL, api_key=config.OPENAI_API_KEY),
    result_type=list[Finding],  # Directly return list of Finding objects
    system_prompt=config.EXTRACTION_SYSTEM_PROMPT,
    retries=2  # Retry up to 2 times on validation errors
)

def extract_findings_from_text(report_text: str) -> list:
    """
    Use Pydantic AI agent to extract findings from a report.
    Automatically retries up to 2 times if extraction fails validation.
    """
    
    # Call Pydantic AI agent - it handles JSON parsing and validation automatically
    result = agent.run_sync(
        f"Extract findings from this report:\n\n{report_text}"
    )
    
    # Result is already a list of Finding objects - no parsing needed!
    return result.data

def main():
    """Main function: read reports, extract findings, save results"""
    
    print("=" * 60)
    print("STEP 1: EXTRACTING FINDINGS FROM REPORTS")
    print("=" * 60)
    
    # Paths
    input_file = Path(config.SAMPLE_REPORTS_FILE)
    output_file = Path(config.EXTRACTED_FINDINGS_FILE)
    
    # Create output directory if needed
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\nReading reports from: {input_file}")
    print(f"Writing results to: {output_file}\n")
    
    # Process each report
    report_count = 0
    
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if not line.strip():
                continue
            
            # Parse the input JSON
            report_data = json.loads(line)
            report_id = report_data.get("report_id")
            report_text = report_data.get("text")
            
            print(f"Processing: {report_id}")
            
            try:
                # Extract findings using Pydantic AI
                findings = extract_findings_from_text(report_text)
                
                print(f"  Extracted {len(findings)} findings")
                
                # Create result object
                result = ExtractionResult(
                    report_id=report_id,
                    findings=findings
                )
                
                # Write to output file
                outfile.write(result.model_dump_json() + "\n")
                
                report_count += 1
                
            except Exception as e:
                print(f"  ERROR: Failed to extract findings from {report_id}")
                print(f"  Error details: {str(e)}")
                # Continue processing other reports
                continue
    
    print(f"\n✓ Complete!")
    print(f"✓ Processed {report_count} reports")
    print(f"✓ Results saved to: {output_file.resolve()}")

if __name__ == "__main__":
    main()
```

## What the Retry Does

When `retries=2` is set:

1. **First attempt**: Agent calls LLM and tries to validate the response
2. **If validation fails**: Agent automatically calls LLM again with error feedback
3. **Second attempt**: LLM gets to see what went wrong and fix it
4. **If still fails**: One more retry
5. **After 2 retries**: Raises exception (caught by your try/except)

## Example Retry Flow
```
Attempt 1:
LLM returns: {findings: [{"name": "kidney stone"}]}  # Missing "present" field
Pydantic AI: "ValidationError: Missing required field 'present'"

Attempt 2:
LLM returns: {findings: [{"name": "kidney stone", "present": true}]}
Pydantic AI: ✅ Valid! Returns list[Finding]
