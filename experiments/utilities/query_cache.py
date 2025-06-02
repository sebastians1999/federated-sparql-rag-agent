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
from entity_indexing.endpoint_loader import query_sparql_wrapper
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
    timeout: Optional[int] = None,
) -> Any:
    """
    Execute a SPARQL query with caching support.
    
    Args:
        query: The SPARQL query
        endpoint_url: The endpoint URL
        use_cache: Whether to check the cache before querying
        update_cache: Whether to update the cache with new results
        cache_dir: The cache directory. If None, uses the default.
        timeout: Timeout for the query in seconds
        
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
    result = query_sparql_wrapper(query, endpoint_url, timeout=timeout)

    
    # Update cache if enabled and the result is not an error
    if update_cache and not isinstance(result, Exception):
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
    endpoint_files_map: Optional[Dict[str, List[str]]] = None,
    timeout: Optional[int] = None
) -> List[dict]:
    """
    Cache all ground truth queries from a dataset.
    
    Args:
        dataset_dir: Directory containing the federated SPARQL dataset
        cache_dir: Directory for the cache. If None, uses the default.
        endpoint_files_map: Dictionary mapping endpoint sets to lists of files to process.
                          e.g., {"Uniprot": ["48_glycosylation_sites_and_glycans.ttl"], "Rhea": []}
        timeout: Optional timeout for SPARQL queries
    Returns:
        List of error dicts for queries that failed to cache
    """
    error_queries = []
    if dataset_dir is None:
        experiments_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dataset_dir = os.path.join(experiments_dir, "federated_sparql_dataset/examples_federated_02.04.2025")
    if cache_dir is None:
        cache_dir = get_cache_dir()

    # Determine endpoint sets and files
    if endpoint_files_map is None:
        endpoint_sets = [d for d in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, d))]
        endpoint_files_map = {endpoint: [] for endpoint in endpoint_sets}

    # Process each endpoint set
    for endpoint_set, file_list in endpoint_files_map.items():
        endpoint_dir = os.path.join(dataset_dir, endpoint_set)
        if not os.path.isdir(endpoint_dir):
            print(endpoint_dir)
            print(f"Warning: Directory for endpoint set '{endpoint_set}' not found")
            continue
        # Process specified files or all files
        if file_list:
            for filename in file_list:
                file_path = os.path.join(endpoint_dir, filename)
                if os.path.isfile(file_path) and file_path.endswith(".ttl"):
                    error = process_ttl_file(file_path, endpoint_set, cache_dir, timeout)
                    if error:
                        error_queries.append(error)
                else:
                    print(f"  Warning: File not found or not a TTL file: {filename}")
        else:
            for root, dirs, files in os.walk(endpoint_dir):
                for file in files:
                    if file.endswith(".ttl"):
                        file_path = os.path.join(root, file)
                        error = process_ttl_file(file_path, endpoint_set, cache_dir, timeout)
                        if error:
                            error_queries.append(error)
    return error_queries





def process_ttl_file(file_path: str, endpoint_set: str, cache_dir: Optional[str], timeout: Optional[int] = None) -> Optional[dict]:
    """
    Helper function to process a TTL file and extract/cache SPARQL queries.
    Returns a dict with error info if an error occurs, otherwise None.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        try:
            meta = get_sparql_question_meta(content)
            query = meta.get("query")
            endpoint_url = meta.get("target_endpoint")
            print("Processing TTL file: " + meta.get("resource"))
            if query and endpoint_url:
                try:
                    result = cached_query_sparql(
                        query, 
                        endpoint_url,
                        use_cache=True,
                        update_cache=True,
                        timeout=timeout,
                        cache_dir=cache_dir
                    )
                    if isinstance(result, Exception):
                        return {"file_path": file_path, "error": str(result)}
                except Exception as e:
                    return {"file_path": file_path, "error": str(e)}
            else:
                return {"file_path": file_path, "error": "Could not extract query or endpoint"}
        except Exception as e:
            return {"file_path": file_path, "error": f"Error parsing TTL with RDFLib: {str(e)} with function get_sparql_question_meta"}
    except Exception as e:
        return {"file_path": file_path, "error": f"Error reading file: {str(e)}"}





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
            except (json.JSONDecodeError, KeyError)as e :
                print(e)
                print(f"Warning: Invalid cache file: {filename}")
                continue
    
    return cached_queries
