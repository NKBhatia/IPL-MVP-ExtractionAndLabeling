import json
from pathlib import Path
import config

def review_extracted_findings():
    """Review and display extracted findings from step 1"""
    
    print("=" * 60)
    print("STEP 0: REVIEW EXTRACTED FINDINGS")
    print("=" * 60)
    
    findings_file = Path(config.EXTRACTED_FINDINGS_FILE)
    
    print(f"\nReading findings from: {findings_file}\n")
    
    if not findings_file.exists():
        print(f"✗ Error: {findings_file} not found")
        return
    
    report_count = 0
    total_findings = 0
    
    with open(findings_file, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            
            findings_data = json.loads(line)
            report_id = findings_data.get("report_id")
            findings = findings_data.get("findings", [])
            
            print(f"Report: {report_id}")
            print(f"  Total findings extracted: {len(findings)}")
            
            for i, finding in enumerate(findings, 1):
                finding_name = finding.get("name", "N/A")
                present = finding.get("present", False)
                status = "✓ Present" if present else "✗ Absent"
                print(f"    {i}. {finding_name} ({status})")
            
            print()
            report_count += 1
            total_findings += len(findings)
    
    print("-" * 60)
    print(f"\n✓ Complete!")
    print(f"✓ Reviewed {report_count} reports")
    print(f"✓ Total findings extracted: {total_findings}")


if __name__ == "__main__":
    review_extracted_findings()