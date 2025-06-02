import time
from typing import List, Dict, Any, Optional
from SPARQLWrapper import SPARQLWrapper, JSON
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import re
from bs4 import BeautifulSoup
import httpx 
import json
import asyncio
import nest_asyncio

def sparql_wrapper_base(
    query: str,
    endpoint_url: str,
    post: bool = False,
    timeout: Optional[int] = 300
) -> Any:
    """
    Execute a SPARQL query against a specified endpoint using SPARQLWrapper.

    This is a low-level function that handles the basic SPARQL query execution with configurable
    HTTP method and timeout settings. Although it uses timeout settings, as long as the endpoint is 
    responsive, the query will not be terminated. for these cases this function is used in 
    query_sparql_wrapper to enforce the timeout.

    Args:
        query: The SPARQL query string to execute
        endpoint_url: URL of the SPARQL endpoint
        post: If True, use HTTP POST method; otherwise use GET (default: False)
        timeout: Maximum time in seconds to wait for the query to complete (default: 300)

    Returns:
        Query results in JSON format if successful, otherwise returns the exception object.
    """
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    if post:
        sparql.setMethod('POST')
    else:
        sparql.setMethod('GET')
    
    if timeout is not None:
        sparql.setTimeout(timeout)
    
    try:
        results = sparql.query().convert()
        return results
    except Exception as e:
        return e





def query_sparql_wrapper(
    query: str,
    endpoint_url: str,
    post: bool = False,
    timeout: Optional[int] = 300
) -> Any:
    """
    Execute a SPARQL query against a specified endpoint using SPARQLWrapper with timeout enforcement.

    This function is a higher-level wrapper that uses asyncio and nest_asyncio to enforce a timeout
    on the SPARQL query execution. It handles the setup of the event loop and ensures that the query
    is terminated if it exceeds the specified timeout.

    Args:
        query: The SPARQL query string to execute
        endpoint_url: URL of the SPARQL endpoint
        post: If True, use HTTP POST method; otherwise use GET (default: False)
        timeout: Maximum time in seconds to wait for the query to complete (default: 300)

    Returns:
        Query results in JSON format if successful, otherwise returns the exception object.
    """
    try:
        asyncio_timeout = timeout + 10 if timeout is not None else 310
        
        # Apply nest_asyncio to allow nesting if an event loop is already running
        nest_asyncio.apply()
        
        try:
            # if a loop is already running (Jupyter)
            loop = asyncio.get_running_loop()
            return loop.run_until_complete(run_with_timeout_enforcement(
                query, endpoint_url, post, timeout, asyncio_timeout
            ))
        except RuntimeError:
            # if no loop is running, use asyncio.run (python script)
            return asyncio.run(run_with_timeout_enforcement(
                query, endpoint_url, post, timeout, asyncio_timeout
            ))
    except Exception as e:
        return e





async def run_with_timeout_enforcement(
    query: str,
    endpoint_url: str,
    post: bool,
    regular_timeout: Optional[int],
    asyncio_timeout: int
) -> Any:
    """
    This function is a helper function for query_sparql_wrapper and is not intended to be called directly.
    
    Args:
        query: The SPARQL query string to execute
        endpoint_url: URL of the SPARQL endpoint
        post: If True, use HTTP POST method; otherwise use GET (default: False)
        regular_timeout: Maximum time in seconds to wait for the query to complete (default: 300)
        asyncio_timeout: Maximum time in seconds to wait for the query to complete (default: 310)
    
    Returns:
        Query results in JSON format if successful, otherwise returns the exception object
    """
    loop = asyncio.get_running_loop()
    
    try:
        return await asyncio.wait_for(
            loop.run_in_executor(
                None,
                lambda: sparql_wrapper_base(query, endpoint_url, post, regular_timeout)
            ),
            timeout=asyncio_timeout
        )
    except asyncio.TimeoutError:
        return Exception(f"Query timed out after {asyncio_timeout} seconds (enforced by asyncio). Results may be partial.")





def retrieve_index_data(entity: dict, entities_list: List[Dict], pagination: tuple = None) -> List[Dict]:
    """
    Retrieve and format entity data from a SPARQL endpoint for indexing.

    This function executes a SPARQL query to fetch entity data and formats it into
    a list of dictionaries suitable for the entity indexing pipeline. This function is
    meant to be a helper function and is used by load_entities_from_endpoints further below.

    Args:
        entity: Dictionary containing entity configuration including 'query' and 'endpoint'.
        entities_list: List to append the retrieved entities to.
        pagination: Optional tuple (limit, offset) for paginated queries.

    Returns:
        List of raw entity results from the SPARQL endpoint, or None if an error occurs
    """
    query = (
        f"{entity['query']} LIMIT {pagination[0]} OFFSET {pagination[1]}"
        if pagination
        else entity["query"]
    )
    try:
        entities_res = sparql_wrapper_base(query, entity["endpoint"])["results"]["bindings"]
    except Exception as e:
        print(f"Error querying endpoint {entity['endpoint']}: {str(e)}")
        return None
    
    print(f"Found {len(entities_res)} entities for {entity['label']} in {entity['endpoint']}")
    #print(f"Entities: {entities_res[:1]}")
    
    for entity_res in entities_res:
        # Create dictionary format compatible with entity_indexing_pipeline_v3.py
        entities_list.append({
            "label": entity_res["label"]["value"],
            "uri": entity_res["uri"]["value"],
            "endpoint_url": entity["endpoint"],
            "entity_type": entity_res["label"]["type"],
            "description": entity.get("description", "")
        })

    return entities_res





def load_entities_from_endpoints(entities_config: List[Dict] = None, max_results_per_batch: int = 200000):

    """
    Load entities from multiple SPARQL endpoints based on the provided configuration.

    This function processes a list of entity configurations, retrieves entities from
    their respective SPARQL endpoints, and returns them in a standardized format.
    Supports pagination for large result sets.

    Args:
        entities_config: List of entity configurations, where each configuration
                       contains query and endpoint information. How such a configuration
                       looks like can be seen in the the entity_indexing/entities_collection.py.
                       
        max_results_per_batch: Maximum number of results to retrieve per batch
                             when pagination is enabled (default: 200000).

    Returns:
        List of dictionaries containing entity data ready for indexing
    """
    
    flattened_configs = []
    start_time = time.time()
    
    if entities_config is not None:
        for entity_group in entities_config:
            if isinstance(entity_group, dict) and any(isinstance(v, dict) for v in entity_group.values()):
                for entity_name, entity_config in entity_group.items():
                    flattened_configs.append(entity_config)
            else:
                flattened_configs.append(entity_group)

    print(f"Flattened {len(flattened_configs)} entities for indexing")
    print(f"Flattened entities: {flattened_configs}")
    
    entities_for_indexing = []
    
    for entity in flattened_configs:
        print(f"Loading entities from {entity['endpoint']} for {entity['label']}...")
        
        if entity.get("pagination", False):
            batch_size = max_results_per_batch
            offset = 0
            batch_results = True
            
            while batch_results:
                batch_results = retrieve_index_data(entity, entities_for_indexing, (batch_size, offset))
                if batch_results:
                    offset += batch_size
                    print(f"  Retrieved {len(batch_results)} entities, total so far: {len(entities_for_indexing)}")
        else:
            retrieve_index_data(entity, entities_for_indexing)
    
    elapsed_time = (time.time() - start_time) / 60
    print(f"Done querying SPARQL endpoints in {elapsed_time:.2f} minutes, retrieved {len(entities_for_indexing)} entities")
    
    return entities_for_indexing
