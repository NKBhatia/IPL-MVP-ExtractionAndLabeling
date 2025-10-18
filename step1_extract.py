import json
import os
from pathlib import Path
from openai import OpenAI
from src.schemas import ExtractionResult, Finding
import config

# Initialize OpenAI client
client = OpenAI(api_key=config.OPENAI_API_KEY)

def extract_findings_from_text(report_text: str) -> list:
    """
    Use OpenAI to extract findings from a report.
    """
    
    # Call OpenAI with the extraction prompt
    response = client.chat.completions.create(
        model=config.EXTRACTION_MODEL,
        messages=[
            {
                "role": "system",
                "content": config.EXTRACTION_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"Extract findings from this report:\n\n{report_text}"
            }
        ],
        temperature=0
    )
    
    # Extract the response text
    response_text = response.choices[0].message.content.strip()
    
    # Remove markdown code fences if present
    clean_response = response_text
    if clean_response.startswith("```json"):
        clean_response = clean_response[7:]
    elif clean_response.startswith("```"):
        clean_response = clean_response[3:]
    
    if clean_response.endswith("```"):
        clean_response = clean_response[:-3]
    
    clean_response = clean_response.strip()
    
    # Parse the JSON response
    try:
        findings_data = json.loads(clean_response)
        
        # Convert to Finding objects
        findings = []
        for item in findings_data:
            finding = Finding(
                name=item.get("name", "").lower(),
                present=item.get("present", False)
            )
            findings.append(finding)
        
        return findings
    
    except json.JSONDecodeError as e:
        print(f"    ERROR: Failed to parse JSON response")
        print(f"    Raw response: {response_text}")
        return []


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
            
            # Extract findings
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
    
    print(f"\n✓ Complete!")
    print(f"✓ Processed {report_count} reports")
    print(f"✓ Results saved to: {output_file.resolve()}")


if __name__ == "__main__":
    main()