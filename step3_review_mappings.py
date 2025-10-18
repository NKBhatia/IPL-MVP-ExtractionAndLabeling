import json
from pathlib import Path
import config

def review_mappings():
    """Review and display mapped findings in a readable format"""
    
    print("=" * 80)
    print("STEP 3: REVIEW MAPPED FINDINGS")
    print("=" * 80)
    
    mapped_file = Path(config.MAPPED_FINDINGS_FILE)
    
    print(f"\nReading mappings from: {mapped_file}\n")
    
    if not mapped_file.exists():
        print(f"✗ Error: {mapped_file} not found")
        return
    
    report_count = 0
    matched_count = 0
    flagged_count = 0
    
    with open(mapped_file, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            
            mapping_data = json.loads(line)
            report_id = mapping_data.get("report_id")
            mapped_findings = mapping_data.get("mapped_findings", [])
            
            print(f"{'='*80}")
            print(f"Report: {report_id}")
            print(f"{'='*80}")
            
            for finding in mapped_findings:
                original = finding.get("original_finding", "N/A")
                mapped_to = finding.get("mapped_to", "N/A")
                model_id = finding.get("model_id", "N/A")
                score = finding.get("confidence_score", 0.0)
                
                # Color code based on threshold
                if mapped_to == "flagged_for_review":
                    status = "⚠️  FLAGGED"
                    flagged_count += 1
                else:
                    status = "✓ MATCHED"
                    matched_count += 1
                
                print(f"\n  {status}")
                print(f"    Original finding: {original}")
                print(f"    Mapped to:       {mapped_to}")
                print(f"    Model ID:        {model_id}")
                print(f"    Confidence:      {score:.3f}")
            
            report_count += 1
            print()
    
    print("=" * 80)
    print(f"\n✓ Complete!")
    print(f"✓ Reviewed {report_count} reports")
    print(f"✓ Matched findings:  {matched_count}")
    print(f"✓ Flagged findings:  {flagged_count}")
    print(f"✓ Match rate:        {(matched_count / (matched_count + flagged_count) * 100):.1f}%\n")


if __name__ == "__main__":
    review_mappings()