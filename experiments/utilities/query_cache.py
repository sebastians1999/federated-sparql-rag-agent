"""
Query cache utility for SPARQL queries.

This module provides functionality to cache SPARQL query results to avoid
repeated queries to endpoints during experimental runs.
"""

import os
import json
import hashlib
import datetime
import pandas as pd
from typing import Any, Dict, Optional, Tuple, List, Union
import httpx

# Import the query_sparql function from endpoint_loader
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from entity_indexing.endpoint_loader import query_sparql
from experiments.utilities.format import get_sparql_question_meta





def get_cache_dir(base_dir: Optional[str] = None) -> str:
    """
    Get the directory for caching query results.
    
    Args:
        base_dir: Base directory for cache. If None, defaults to 'experiments/federated_sparql_dataset/query_cache'
        
    Returns:
        Path to the cache directory
    """
    if base_dir is None:
        # Get the experiments directory
        experiments_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base_dir = os.path.join(experiments_dir, "federated_sparql_dataset", "query_cache")
    
    # Ensure the cache directory exists
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        
    return base_dir


def generate_cache_key(query: str, endpoint_url: str) -> str:
    """
    Generate a unique cache key for a query and endpoint combination.
    
    Args:
        query: The SPARQL query
        endpoint_url: The endpoint URL
        
    Returns:
        A hash string to use as the cache key
    """
    # Combine query and endpoint to create a unique identifier
    combined = f"{endpoint_url}:{query}"
    # Create a hash of the combined string
    hash_obj = hashlib.md5(combined.encode())
    return hash_obj.hexdigest()


def get_cache_path(cache_key: str, cache_dir: Optional[str] = None) -> str:
    """
    Get the full path to a cache file.
    
    Args:
        cache_key: The cache key (hash)
        cache_dir: The cache directory. If None, uses the default.
        
    Returns:
        Full path to the cache file
    """
    cache_dir = get_cache_dir(cache_dir)
    return os.path.join(cache_dir, f"{cache_key}.json")


def save_to_cache(query: str, endpoint_url: str, result: Any, cache_dir: Optional[str] = None) -> str:
    """
    Save a query result to the cache.
    
    Args:
        query: The SPARQL query
        endpoint_url: The endpoint URL
        result: The query result to cache
        cache_dir: The cache directory. If None, uses the default.
        
    Returns:
        Path to the cache file
    """
    cache_key = generate_cache_key(query, endpoint_url)
    cache_path = get_cache_path(cache_key, cache_dir)
    
    # Create a cache entry with metadata
    cache_entry = {
        "query": query,
        "endpoint_url": endpoint_url,
        "timestamp": datetime.datetime.now().isoformat(),
        "result": result
    }
    
    # Save to file
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(cache_entry, f, ensure_ascii=False, indent=2)
    
    return cache_path


def load_from_cache(query: str, endpoint_url: str, cache_dir: Optional[str] = None) -> Optional[Any]:
    """
    Load a query result from the cache if it exists.
    
    Args:
        query: The SPARQL query
        endpoint_url: The endpoint URL
        cache_dir: The cache directory. If None, uses the default.
        
    Returns:
        The cached result or None if not found
    """
    cache_key = generate_cache_key(query, endpoint_url)
    cache_path = get_cache_path(cache_key, cache_dir)
    
    if os.path.exists(cache_path):
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_entry = json.load(f)
            return cache_entry["result"]
        except (json.JSONDecodeError, KeyError):
            # If there's an issue with the cache file, return None
            return None
    
    return None


def cached_query_sparql(
    query: str,
    endpoint_url: str,
    use_cache: bool = True,
    update_cache: bool = True,
    cache_dir: Optional[str] = None,
) -> Any:
    """
    Execute a SPARQL query with caching support.
    
    Args:
        query: The SPARQL query
        endpoint_url: The endpoint URL
        use_cache: Whether to check the cache before querying
        update_cache: Whether to update the cache with new results
        cache_dir: The cache directory. If None, uses the default.
        
    Returns:
        Query result or error information
    """
    # Check cache first if enabled
    if use_cache:
        cached_result = load_from_cache(query, endpoint_url, cache_dir)
        if cached_result is not None:
            print(f"  Using cached result for query")
            return cached_result
    print(f"  Querying endpoint: {endpoint_url}")
    # If not in cache or cache disabled, execute the query
    result = query_sparql(query, endpoint_url)

    #print(f"  Query result: {result}")
    
    # Update cache if enabled and the result is not an error
    if update_cache and (isinstance(result, dict) and result != "error"):
        save_to_cache(query, endpoint_url, result, cache_dir)
    
    return result


def format_query_result_dataframe(
    ground_truth_query: str,
    ground_truth_endpoint: str,
    use_cache: bool = True,
    update_cache: bool = True,
    cache_dir: Optional[str] = None
) -> pd.DataFrame:
    """
    Format SPARQL query results as pandas DataFrames with caching support.
    
    Args:
        ground_truth_query: The ground truth SPARQL query
        ground_truth_endpoint: The endpoint URL for ground truth
        use_cache: Whether to use cached results
        update_cache: Whether to update the cache with new results
        cache_dir: The cache directory. If None, uses the default.
        
    Returns:
        DataFrame containing the formatted query results
    """
    # Query ground truth with caching
    ground_truth = cached_query_sparql(
        ground_truth_query, 
        ground_truth_endpoint,
        use_cache=use_cache,
        update_cache=update_cache,
        cache_dir=cache_dir
    )
    
    # Process ground truth results
    df_ground_truth = pd.DataFrame()
    if isinstance(ground_truth, dict) and ground_truth != "error":
        processed_data = []
        bindings_ground_truth = ground_truth['results']['bindings']
        for row_binding in bindings_ground_truth:
            processed_row = {}
            for var_name, value_dict in row_binding.items():
                if isinstance(value_dict, dict) and 'value' in value_dict:
                    processed_row[var_name] = value_dict['value']
                else:
                    processed_row[var_name] = None
            processed_data.append(processed_row)
        df_ground_truth = pd.DataFrame(processed_data)
    
    return df_ground_truth


def cache_dataset_queries(
    dataset_dir: Optional[str] = None,
    cache_dir: Optional[str] = None,
    endpoint_files_map: Optional[Dict[str, List[str]]] = None
) -> Dict[str, int]:
    """
    Cache all ground truth queries from a dataset.
    
    Args:
        dataset_dir: Directory containing the federated SPARQL dataset
        cache_dir: Directory for the cache. If None, uses the default.
        endpoint_files_map: Dictionary mapping endpoint sets to lists of files to process.
                          e.g., {"Uniprot": ["48_glycosylation_sites_and_glycans.ttl"], "Rhea": []}
                          If an empty list is provided for an endpoint, all files in that endpoint will be processed.
                          If None, processes all files in all endpoints.
        
    Returns:
        Dictionary with counts of cached queries per endpoint
    """
    # Set defaults if not provided
    if dataset_dir is None:
        # Get the experiments directory
        experiments_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dataset_dir = os.path.join(experiments_dir, "federated_sparql_dataset/examples_federated_02.04.2025")
    
    # Get all endpoint sets if not specified
    if endpoint_files_map is None:
        endpoint_sets = [d for d in os.listdir(dataset_dir) 
                         if os.path.isdir(os.path.join(dataset_dir, d))]
        endpoint_files_map = {endpoint: [] for endpoint in endpoint_sets}  # Empty list means process all files
    
    # Initialize statistics
    stats = {endpoint: 0 for endpoint in endpoint_files_map.keys()}
    total_cached = 0
    
    # Process each endpoint set
    for endpoint_set, file_list in endpoint_files_map.items():
        print(f"Processing endpoint set: {endpoint_set}")
        
        # Find the directory for this endpoint set
        endpoint_dir = os.path.join(dataset_dir, endpoint_set)
        if not os.path.isdir(endpoint_dir):
            print(f"Warning: Directory for endpoint set '{endpoint_set}' not found")
            continue
        
        # Process specified files or all files in this endpoint directory
        if file_list:  # If specific files are provided
            print(f"  Processing {len(file_list)} specified files")
            for filename in file_list:
                file_path = os.path.join(endpoint_dir, filename)
                if os.path.isfile(file_path) and file_path.endswith(".ttl"):
                    print(f"  Processing TTL file: {filename}")
                    process_ttl_file(file_path, endpoint_set, cache_dir, stats, total_cached)
                else:
                    print(f"  Warning: File not found or not a TTL file: {filename}")
        else:  # Process all files
            print(f"  Processing all files in {endpoint_set}")
            for root, dirs, files in os.walk(endpoint_dir):
                for file in files:
                    if file.endswith(".ttl"):
                        file_path = os.path.join(root, file)
                        process_ttl_file(file_path, endpoint_set, cache_dir, stats, total_cached)
    
    # Print summary
    print(f"\nCaching complete. Total queries cached: {sum(stats.values())}")
    for endpoint, count in stats.items():
        print(f"  {endpoint}: {count} queries")
    
    return stats


def process_ttl_file(file_path: str, endpoint_set: str, cache_dir: Optional[str], stats: Dict[str, int], total_cached: int) -> None:
    """Helper function to process a TTL file and extract/cache SPARQL queries."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        try:
            meta = get_sparql_question_meta(content)
            query = meta.get("query")
            endpoint_url = meta.get("target_endpoint")
            print("Processing TTL file: " + meta.get("resource"))
            
            # If we found both query and endpoint, cache the result
            if query and endpoint_url:
                try:
                    #print(f"  Caching query: {query}")
                    # Query and cache the result
                    result = cached_query_sparql(
                        query, 
                        endpoint_url,
                        use_cache=True,
                        update_cache=True,
                        cache_dir=cache_dir
                    )
                    
                    # Update statistics
                    if isinstance(result, dict) and result != "error":
                        stats[endpoint_set] += 1
                        #print(f"  Cached query from {os.path.basename(file_path)}")
                    else:
                        print(f"  Error executing query from {os.path.basename(file_path)}: {result}")
                except Exception as e:
                    print(f"  Error processing {os.path.basename(file_path)}: {str(e)}")
            else:
                print(f"  Could not extract query or endpoint from {os.path.basename(file_path)}")
        except Exception as e:
            print(f"  Error parsing TTL with RDFLib in {os.path.basename(file_path)}: {str(e)} with function get_sparql_question_meta")
    except Exception as e:
        print(f"  Error reading {os.path.basename(file_path)}: {str(e)}")



def list_cached_queries(cache_dir: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List all cached queries with their metadata.
    
    Args:
        cache_dir: The cache directory. If None, uses the default.
        
    Returns:
        List of dictionaries with query metadata
    """
    cache_dir = get_cache_dir(cache_dir)
    
    cached_queries = []
    
    # Iterate through all files in the cache directory
    for filename in os.listdir(cache_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(cache_dir, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    cache_entry = json.load(f)
                
                # Add metadata to the list
                cached_queries.append({
                    "query": cache_entry.get("query", ""),
                    "endpoint_url": cache_entry.get("endpoint_url", ""),
                    "timestamp": cache_entry.get("timestamp", ""),
                    "cache_file": filename,
                    "has_results": "results" in cache_entry.get("result", {})
                })
            except (json.JSONDecodeError, KeyError):
                # Skip invalid cache files
                continue
    
    return cached_queries
