import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from experiments.utilities.query_cache import cache_dataset_queries

if __name__ == "__main__":
    result = cache_dataset_queries(
        endpoint_files_map={
            "UniProt": [],
            "Rhea": [],
            "SwissLipids": []
        }
    )
    print("Caching completed.")