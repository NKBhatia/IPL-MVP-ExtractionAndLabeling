import json
import numpy as np
from pathlib import Path
from openai import OpenAI
import config

# Initialize OpenAI client
client = OpenAI(api_key=config.OPENAI_API_KEY)

def load_finding_models(filepath="data/finding_models.json"):
    """Load finding models from local JSON file"""
    try:
        with open(filepath, 'r') as f:
            models = json.load(f)
        print(f"✓ Loaded {len(models)} finding models")
        return models
    except FileNotFoundError:
        print(f"✗ Error: {filepath} not found")
        return []
    except json.JSONDecodeError:
        print(f"✗ Error: {filepath} is not valid JSON")
        return []


def create_embeddings(texts):
    """Create embeddings for a list of texts using OpenAI"""
    if not texts:
        return []
    
    response = client.embeddings.create(
        model=config.EMBEDDING_MODEL,
        input=texts
    )
    
    return [item.embedding for item in response.data]


def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    dot_product = np.dot(vec1, vec2)
    norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    
    if norm_product == 0:
        return 0.0
    
    return dot_product / norm_product


def map_finding_to_model(finding_name, model_embeddings, models, threshold=0.70):
    """
    Map a single finding to the best matching finding model.
    Returns the best match and confidence score.
    """
    # Create embedding for the finding
    finding_embedding = create_embeddings([finding_name])[0]
    
    best_match = None
    best_score = 0.0
    
    # Compare against all models
    for i, model_embedding in enumerate(model_embeddings):
        score = cosine_similarity(finding_embedding, model_embedding)
        
        if score > best_score:
            best_score = score
            best_match = models[i]
    
    # Return result
    if best_score >= threshold:
        return {
            "matched_model": best_match["name"],
            "model_id": best_match.get("oifm_id", "N/A"),
            "score": round(best_score, 3)
        }
    else:
        return {
            "matched_model": "flagged_for_review",
            "model_id": "N/A",
            "score": round(best_score, 3)
        }


def main():
    """Main function: load findings and map to models"""
    
    print("=" * 60)
    print("STEP 2: MAPPING FINDINGS TO MODELS")
    print("=" * 60)
    
    # Paths
    findings_file = Path(config.EXTRACTED_FINDINGS_FILE)
    models_file = Path("data/finding_models.json")
    output_file = Path(config.MAPPED_FINDINGS_FILE)
    
    print(f"\nReading findings from: {findings_file}")
    print(f"Reading models from: {models_file}")
    print(f"Writing results to: {output_file}\n")
    
    # Load finding models
    print("[1/3] Loading finding models...")
    models = load_finding_models(models_file)
    
    if not models:
        print("✗ No models loaded. Exiting.")
        return
    
    # Create embeddings for all models
    print("\n[2/3] Creating embeddings for models...")
    model_names_and_descriptions = [
        f"{model['name']}. {model['description']}" for model in models
    ]
    
    model_embeddings = create_embeddings(model_names_and_descriptions)
    print(f"✓ Created {len(model_embeddings)} model embeddings")
    
    # Map findings
    print("\n[3/3] Mapping findings to models...")
    print("-" * 60)
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    report_count = 0
    total_mappings = 0
    
    with open(findings_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if not line.strip():
                continue
            
            # Parse the extracted findings
            findings_data = json.loads(line)
            report_id = findings_data.get("report_id")
            findings = findings_data.get("findings", [])
            
            print(f"\nMapping findings for: {report_id}")
            
            # Map each finding
            mapped_findings = []
            for finding in findings:
                finding_name = finding.get("name", "")
                
                # Skip if finding name is empty
                if not finding_name:
                    continue
                
                # Map to model
                result = map_finding_to_model(
                    finding_name,
                    model_embeddings,
                    models,
                    threshold=0.70
                )
                
                print(f"  Mapping: {finding_name}")
                print(f"    → {result['matched_model']} (score: {result['score']})")
                
                mapped_findings.append({
                    "original_finding": finding_name,
                    "mapped_to": result["matched_model"],
                    "model_id": result["model_id"],
                    "confidence_score": result["score"]
                })
                
                total_mappings += 1
            
            # Write to output
            output_data = {
                "report_id": report_id,
                "mapped_findings": mapped_findings
            }
            
            outfile.write(json.dumps(output_data) + "\n")
            report_count += 1
    
    print("\n" + "-" * 60)
    print(f"\n✓ Complete!")
    print(f"✓ Mapped {report_count} reports")
    print(f"✓ Total mappings: {total_mappings}")
    print(f"✓ Results saved to: {output_file}")


if __name__ == "__main__":
    main()