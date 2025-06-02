from query_cache import cache_dataset_queries



"""
Pre-caches SPARQL query results from the evaluation dataset to improve performance during experiments.

This script caches the results of SPARQL queries to avoid repeated long-running executions 
during evaluation. By default, it caches all 32 SPARQL queries from the evaluation set.

Usage:
    - Run the script as-is to cache all queries for all endpoints
    - Modify `endpoint_files_map` to cache specific queries:
        - Empty lists (default): Cache all queries for that endpoint
        - Specific files: Cache only listed queries (e.g., ["6.ttl"])
        - Omit endpoint: Don't cache any queries for that endpoint

Cached results are stored in: 
    experiments/federated_sparql_dataset/query_cache/
    (as individual JSON files with UUID-based names)

Example:
    To cache only query 6.ttl from SwissLipids:
    endpoint_files_map = {"SwissLipids": ["6.ttl"]}
"""


if __name__ == "__main__":
    result = cache_dataset_queries(
        endpoint_files_map={
            "UniProt": [],
            "Rhea": [],
            "SwissLipids": []
        }
    )
    print("Caching completed.")