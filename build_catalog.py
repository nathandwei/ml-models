#!/usr/bin/env python3
"""Auto-generates catalog.yaml from week metadata files."""

import yaml
from pathlib import Path

def build_catalog():
    models_dir = Path("Models")
    if not models_dir.exists():
        models_dir.mkdir()
        print("Created Models/ directory")
        return
    
    models = []
    
    for week_folder in sorted(models_dir.iterdir()):
        if not week_folder.is_dir():
            continue
            
        metadata_file = week_folder / "metadata.yaml"
        if not metadata_file.exists():
            continue
            
        with open(metadata_file) as f:
            meta = yaml.safe_load(f) or {}
        
        model_entry = {
            "week": meta.get("week"),
            "path": str(week_folder),
            "dataset": meta.get("dataset"),
            "model_type": meta.get("model_type"),
            "techniques": meta.get("techniques", []),
            "date": meta.get("date"),
        }
        
        if "metrics" in meta:
            model_entry["metrics"] = meta["metrics"]
        if "notes" in meta:
            model_entry["notes"] = meta["notes"]
            
        models.append(model_entry)
    
    with open("catalog.yaml", "w") as f:
        yaml.dump({"models": models}, f, default_flow_style=False, sort_keys=False)
    
    print(f"✓ Built catalog with {len(models)} models")

if __name__ == "__main__":
    build_catalog()
