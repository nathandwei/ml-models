#!/usr/bin/env python3
"""Query models from catalog by dataset, model_type, or technique."""

import yaml
import sys

def query_models(filter_key, filter_value):
    try:
        with open('catalog.yaml') as f:
            catalog = yaml.safe_load(f)
    except FileNotFoundError:
        print("catalog.yaml not found. Run: python build_catalog.py")
        return
    
    matches = []
    for model in catalog.get('models', []):
        if filter_key == 'technique':
            if filter_value in model.get('techniques', []):
                matches.append(model)
        elif model.get(filter_key) == filter_value:
            matches.append(model)
    
    if not matches:
        print(f"No models found with {filter_key}='{filter_value}'")
        return
    
    print(f"Found {len(matches)} model(s):\n")
    for model in matches:
        print(f"Week {model['week']}: {model['path']}")
        print(f"  Dataset: {model.get('dataset')}")
        print(f"  Model: {model.get('model_type')}")
        print(f"  Techniques: {', '.join(model.get('techniques', []))}")
        if 'metrics' in model:
            print(f"  Metrics: {model['metrics']}")
        if 'notes' in model:
            print(f"  Notes: {model['notes'][:80]}...")
        print()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python query_models.py <filter_key> <filter_value>")
        print("Examples:")
        print("  python query_models.py model_type xgboost")
        print("  python query_models.py dataset iris")
        print("  python query_models.py technique smote")
        sys.exit(1)
    
    query_models(sys.argv[1], sys.argv[2])
